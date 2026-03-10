import uuid
from flask import render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_required, current_user
from app.blueprints.main import main_bp
from app.extensions import db
from app.models import (Product, Category, Review, CartItem, WishlistItem,
                        Order, OrderItem, Newsletter)


@main_bp.route('/')
def index():
    featured = Product.query.filter_by(is_featured=True, is_active=True).limit(8).all()
    categories = Category.query.filter_by(is_active=True).all()
    latest = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(4).all()
    return render_template('main/index.html', featured=featured, categories=categories, latest=latest)


@main_bp.route('/shop')
def shop():
    page = request.args.get('page', 1, type=int)
    category_slug = request.args.get('category', '')
    sort = request.args.get('sort', 'newest')
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 99999, type=float)
    search_q = request.args.get('q', '').strip()

    query = Product.query.filter_by(is_active=True)

    if category_slug:
        cat = Category.query.filter_by(slug=category_slug).first()
        if cat:
            query = query.filter_by(category_id=cat.id)

    if min_price > 0:
        query = query.filter(Product.price >= min_price)
    if max_price < 99999:
        query = query.filter(Product.price <= max_price)

    if search_q:
        query = query.filter(
            db.or_(
                Product.name.ilike(f'%{search_q}%'),
                Product.description.ilike(f'%{search_q}%'),
                Product.brand.ilike(f'%{search_q}%')
            )
        )

    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'name':
        query = query.order_by(Product.name.asc())
    else:
        query = query.order_by(Product.created_at.desc())

    products = query.paginate(page=page, per_page=12, error_out=False)
    categories = Category.query.filter_by(is_active=True).all()

    return render_template('main/shop.html', products=products, categories=categories,
                           current_category=category_slug, current_sort=sort,
                           min_price=min_price, max_price=max_price, search_q=search_q)


@main_bp.route('/product/<slug>')
def product_detail(slug):
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    related = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()
    reviews = product.reviews.order_by(Review.created_at.desc()).all()

    in_wishlist = False
    if current_user.is_authenticated:
        in_wishlist = WishlistItem.query.filter_by(
            user_id=current_user.id, product_id=product.id
        ).first() is not None

    return render_template('main/product.html', product=product, related=related,
                           reviews=reviews, in_wishlist=in_wishlist)


@main_bp.route('/product/<int:product_id>/review', methods=['POST'])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    existing = Review.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        flash('You have already reviewed this product.', 'warning')
        return redirect(url_for('main.product_detail', slug=product.slug))

    rating = request.form.get('rating', 5, type=int)
    title = request.form.get('title', '').strip()
    comment = request.form.get('comment', '').strip()

    if rating < 1 or rating > 5:
        rating = 5

    review = Review(user_id=current_user.id, product_id=product_id,
                    rating=rating, title=title, comment=comment)
    db.session.add(review)
    db.session.commit()
    flash('Your review has been submitted.', 'success')
    return redirect(url_for('main.product_detail', slug=product.slug))


# ---- CART ----
@main_bp.route('/cart')
def cart():
    cart_items = []
    total = 0
    if current_user.is_authenticated:
        items = CartItem.query.filter_by(user_id=current_user.id).all()
        for item in items:
            subtotal = item.product.price * item.quantity
            cart_items.append({'item': item, 'product': item.product, 'quantity': item.quantity, 'subtotal': subtotal})
            total += subtotal
    else:
        cart_data = session.get('cart', {})
        for pid_str, qty in cart_data.items():
            product = Product.query.get(int(pid_str))
            if product:
                subtotal = product.price * qty
                cart_items.append({'product': product, 'quantity': qty, 'subtotal': subtotal, 'item': None})
                total += subtotal
    return render_template('main/cart.html', cart_items=cart_items, total=total)


@main_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    if quantity < 1:
        quantity = 1

    product = Product.query.get_or_404(product_id)
    if product.stock < quantity:
        flash('Not enough stock available.', 'warning')
        return redirect(request.referrer or url_for('main.shop'))

    if current_user.is_authenticated:
        existing = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if existing:
            existing.quantity += quantity
        else:
            ci = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
            db.session.add(ci)
        db.session.commit()
    else:
        cart_data = session.get('cart', {})
        pid_str = str(product_id)
        cart_data[pid_str] = cart_data.get(pid_str, 0) + quantity
        session['cart'] = cart_data

    flash(f'{product.name} added to cart.', 'success')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        count = 0
        if current_user.is_authenticated:
            count = CartItem.query.filter_by(user_id=current_user.id).count()
        else:
            count = len(session.get('cart', {}))
        return jsonify({'success': True, 'cart_count': count})

    return redirect(request.referrer or url_for('main.shop'))


@main_bp.route('/cart/update', methods=['POST'])
def update_cart():
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)

    if quantity < 1:
        return remove_from_cart()

    if current_user.is_authenticated:
        item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if item:
            item.quantity = quantity
            db.session.commit()
    else:
        cart_data = session.get('cart', {})
        cart_data[str(product_id)] = quantity
        session['cart'] = cart_data

    flash('Cart updated.', 'success')
    return redirect(url_for('main.cart'))


@main_bp.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id', type=int)

    if current_user.is_authenticated:
        item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
    else:
        cart_data = session.get('cart', {})
        cart_data.pop(str(product_id), None)
        session['cart'] = cart_data

    flash('Item removed from cart.', 'info')
    return redirect(url_for('main.cart'))


# ---- CHECKOUT ----
@main_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('main.shop'))

    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        order_number = f"SW-{uuid.uuid4().hex[:8].upper()}"
        order = Order(
            user_id=current_user.id,
            order_number=order_number,
            total_amount=total,
            shipping_address=request.form.get('address', ''),
            shipping_city=request.form.get('city', ''),
            shipping_state=request.form.get('state', ''),
            shipping_zip=request.form.get('zip_code', ''),
            shipping_country=request.form.get('country', ''),
            shipping_phone=request.form.get('phone', ''),
            status='pending',
            payment_status='unpaid'
        )
        db.session.add(order)
        db.session.flush()

        for item in cart_items:
            oi = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(oi)
            item.product.stock -= item.quantity

        db.session.commit()
        session['pending_order_id'] = order.id
        return redirect(url_for('payment.initialize', order_id=order.id))

    from flask import current_app
    paystack_public = current_app.config.get('PAYSTACK_PUBLIC_KEY', '')
    return render_template('main/checkout.html', cart_items=cart_items, total=total,
                           paystack_public=paystack_public)


@main_bp.route('/order-confirmation/<order_number>')
@login_required
def order_confirmation(order_number):
    order = Order.query.filter_by(order_number=order_number, user_id=current_user.id).first_or_404()
    return render_template('main/order_confirmation.html', order=order)


@main_bp.route('/orders')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('main/orders.html', orders=orders)


@main_bp.route('/order/<order_number>')
@login_required
def order_detail(order_number):
    order = Order.query.filter_by(order_number=order_number, user_id=current_user.id).first_or_404()
    return render_template('main/order_detail.html', order=order)


# ---- WISHLIST ----
@main_bp.route('/wishlist')
@login_required
def wishlist():
    items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    return render_template('main/wishlist.html', items=items)


@main_bp.route('/wishlist/toggle', methods=['POST'])
@login_required
def toggle_wishlist():
    product_id = request.form.get('product_id', type=int)
    existing = WishlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash('Removed from wishlist.', 'info')
        status = 'removed'
    else:
        wi = WishlistItem(user_id=current_user.id, product_id=product_id)
        db.session.add(wi)
        db.session.commit()
        flash('Added to wishlist.', 'success')
        status = 'added'

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'status': status})
    return redirect(request.referrer or url_for('main.wishlist'))


# ---- SEARCH ----
@main_bp.route('/search')
def search():
    q = request.args.get('q', '').strip()
    if not q:
        return redirect(url_for('main.shop'))
    return redirect(url_for('main.shop', q=q))


@main_bp.route('/api/search-suggestions')
def search_suggestions():
    q = request.args.get('q', '').strip()
    if len(q) < 2:
        return jsonify([])
    products = Product.query.filter(
        Product.is_active == True,
        db.or_(
            Product.name.ilike(f'%{q}%'),
            Product.brand.ilike(f'%{q}%')
        )
    ).limit(5).all()
    results = [{'id': p.id, 'name': p.name, 'price': p.price, 'slug': p.slug,
                'image': p.image_url, 'brand': p.brand} for p in products]
    return jsonify(results)


# ---- NEWSLETTER ----
@main_bp.route('/newsletter', methods=['POST'])
def newsletter_signup():
    email = request.form.get('email', '').strip().lower()
    if not email:
        flash('Please enter your email.', 'warning')
        return redirect(request.referrer or url_for('main.index'))

    existing = Newsletter.query.filter_by(email=email).first()
    if existing:
        flash('You are already subscribed!', 'info')
    else:
        nl = Newsletter(email=email)
        db.session.add(nl)
        db.session.commit()
        flash('Thank you for subscribing!', 'success')

    return redirect(request.referrer or url_for('main.index'))
