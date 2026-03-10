from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.blueprints.auth import auth_bp
from app.extensions import db
from app.models import User
import re


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()

        errors = []
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters.')
        if not email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors.append('Please enter a valid email address.')
        if not password or len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if password != confirm_password:
            errors.append('Passwords do not match.')
        if User.query.filter_by(username=username).first():
            errors.append('Username is already taken.')
        if User.query.filter_by(email=email).first():
            errors.append('Email is already registered.')

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('auth/signup.html', username=username, email=email,
                                   first_name=first_name, last_name=last_name)

        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash('Welcome to Smart Watches! Your account has been created.', 'success')
        next_page = request.args.get('next')
        return redirect(next_page or url_for('main.index'))

    return render_template('auth/signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            if not user.is_active_user:
                flash('Your account has been disabled. Please contact support.', 'danger')
                return render_template('auth/login.html', email=email)

            login_user(user, remember=bool(remember))
            flash(f'Welcome back, {user.full_name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')
            return render_template('auth/login.html', email=email)

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name', '').strip()
        current_user.last_name = request.form.get('last_name', '').strip()
        current_user.phone = request.form.get('phone', '').strip()
        current_user.address = request.form.get('address', '').strip()
        current_user.city = request.form.get('city', '').strip()
        current_user.state = request.form.get('state', '').strip()
        current_user.zip_code = request.form.get('zip_code', '').strip()
        current_user.country = request.form.get('country', '').strip()
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('auth/profile.html')
