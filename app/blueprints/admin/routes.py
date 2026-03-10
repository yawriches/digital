from functools import wraps
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.blueprints.admin import admin_bp
from app.extensions import db
from app.models import Product, Category, Order, OrderItem, User, Newsletter, Review
from datetime import datetime, timedelta
import re


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/')
@admin_required
def dashboard():
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter(
        Order.payment_status == 'paid'
    ).scalar() or 0
    total_customers = User.query.filter_by(is_admin=False).count()
    total_products = Product.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    low_stock = Product.query.filter(Product.stock < 5).count()

    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()

    today = datetime.utcnow().date()
    revenue_data = []
    labels = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time())
        day_end = datetime.combine(day, datetime.max.time())
        day_revenue = db.session.query(db.func.sum(Order.total_amount)).filter(
            Order.created_at.between(day_start, day_end),
            Order.payment_status == 'paid'
        ).scalar() or 0
        revenue_data.append(float(day_revenue))
        labels.append(day.strftime('%b %d'))

    status_counts = {}
    for status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
        status_counts[status] = Order.query.filter_by(status=status).count()

    return render_template('admin/dashboard.html',
                           total_orders=total_orders, total_revenue=total_revenue,
                           total_customers=total_customers, total_products=total_products,
                           pending_orders=pending_orders, low_stock=low_stock,
                           recent_orders=recent_orders, revenue_data=revenue_data,
                           labels=labels, status_counts=status_counts)


# ---- PRODUCTS ----
@admin_bp.route('/products')
@admin_required
def products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/products.html', products=products)


@admin_bp.route('/products/add', methods=['GET', 'POST'])
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        existing_slug = Product.query.filter_by(slug=slug).first()
        if existing_slug:
            slug = slug + '-' + str(Product.query.count() + 1)

        sku = request.form.get('sku', '').strip()
        if not sku:
            sku = f"SW-{Product.query.count() + 1:04d}"

        product = Product(
            name=name,
            slug=slug,
            description=request.form.get('description', ''),
            short_description=request.form.get('short_description', ''),
            price=float(request.form.get('price', 0)),
            compare_price=float(request.form.get('compare_price', 0) or 0),
            stock=int(request.form.get('stock', 0)),
            sku=sku,
            category_id=int(request.form.get('category_id', 1)),
            image_url=request.form.get('image_url', ''),
            image_url_2=request.form.get('image_url_2', ''),
            image_url_3=request.form.get('image_url_3', ''),
            is_featured=bool(request.form.get('is_featured')),
            is_active=bool(request.form.get('is_active', True)),
            brand=request.form.get('brand', ''),
            specifications=request.form.get('specifications', '')
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully.', 'success')
        return redirect(url_for('admin.products'))

    categories = Category.query.filter_by(is_active=True).all()
    return render_template('admin/product_form.html', product=None, categories=categories)


@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form.get('name', '').strip()
        product.description = request.form.get('description', '')
        product.short_description = request.form.get('short_description', '')
        product.price = float(request.form.get('price', 0))
        product.compare_price = float(request.form.get('compare_price', 0) or 0)
        product.stock = int(request.form.get('stock', 0))
        product.sku = request.form.get('sku', product.sku)
        product.category_id = int(request.form.get('category_id', product.category_id))
        product.image_url = request.form.get('image_url', '')
        product.image_url_2 = request.form.get('image_url_2', '')
        product.image_url_3 = request.form.get('image_url_3', '')
        product.is_featured = bool(request.form.get('is_featured'))
        product.is_active = bool(request.form.get('is_active'))
        product.brand = request.form.get('brand', '')
        product.specifications = request.form.get('specifications', '')
        db.session.commit()
        flash('Product updated successfully.', 'success')
        return redirect(url_for('admin.products'))

    categories = Category.query.filter_by(is_active=True).all()
    return render_template('admin/product_form.html', product=product, categories=categories)


@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'info')
    return redirect(url_for('admin.products'))


# ---- ORDERS ----
@admin_bp.route('/orders')
@admin_required
def orders():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    query = Order.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    orders = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/orders.html', orders=orders, status_filter=status_filter)


@admin_bp.route('/orders/<int:order_id>')
@admin_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)


@admin_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = request.form.get('status', order.status)
    db.session.commit()
    flash(f'Order #{order.order_number} status updated to {order.status}.', 'success')
    return redirect(url_for('admin.order_detail', order_id=order.id))


# ---- CUSTOMERS ----
@admin_bp.route('/customers')
@admin_required
def customers():
    page = request.args.get('page', 1, type=int)
    users = User.query.filter_by(is_admin=False).order_by(User.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/customers.html', users=users)


@admin_bp.route('/customers/<int:user_id>/toggle', methods=['POST'])
@admin_required
def toggle_customer(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        flash('Cannot disable an admin account.', 'danger')
        return redirect(url_for('admin.customers'))
    user.is_active_user = not user.is_active_user
    db.session.commit()
    status = 'enabled' if user.is_active_user else 'disabled'
    flash(f'User {user.username} has been {status}.', 'success')
    return redirect(url_for('admin.customers'))


# ---- CATEGORIES ----
@admin_bp.route('/categories')
@admin_required
def categories():
    cats = Category.query.order_by(Category.name).all()
    return render_template('admin/categories.html', categories=cats)


@admin_bp.route('/categories/add', methods=['POST'])
@admin_required
def add_category():
    name = request.form.get('name', '').strip()
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    description = request.form.get('description', '')
    image_url = request.form.get('image_url', '')

    if Category.query.filter_by(slug=slug).first():
        flash('Category already exists.', 'warning')
        return redirect(url_for('admin.categories'))

    cat = Category(name=name, slug=slug, description=description, image_url=image_url)
    db.session.add(cat)
    db.session.commit()
    flash('Category added.', 'success')
    return redirect(url_for('admin.categories'))


@admin_bp.route('/categories/edit/<int:cat_id>', methods=['POST'])
@admin_required
def edit_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    cat.name = request.form.get('name', cat.name).strip()
    cat.description = request.form.get('description', '')
    cat.image_url = request.form.get('image_url', '')
    cat.is_active = bool(request.form.get('is_active'))
    db.session.commit()
    flash('Category updated.', 'success')
    return redirect(url_for('admin.categories'))


@admin_bp.route('/categories/delete/<int:cat_id>', methods=['POST'])
@admin_required
def delete_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    if cat.products.count() > 0:
        flash('Cannot delete a category with products.', 'danger')
        return redirect(url_for('admin.categories'))
    db.session.delete(cat)
    db.session.commit()
    flash('Category deleted.', 'info')
    return redirect(url_for('admin.categories'))


# ---- API for dashboard charts ----
@admin_bp.route('/api/stats')
@admin_required
def api_stats():
    today = datetime.utcnow().date()
    revenue_data = []
    labels = []
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        day_start = datetime.combine(day, datetime.min.time())
        day_end = datetime.combine(day, datetime.max.time())
        day_revenue = db.session.query(db.func.sum(Order.total_amount)).filter(
            Order.created_at.between(day_start, day_end),
            Order.payment_status == 'paid'
        ).scalar() or 0
        revenue_data.append(float(day_revenue))
        labels.append(day.strftime('%b %d'))

    return jsonify({'labels': labels, 'revenue': revenue_data})
