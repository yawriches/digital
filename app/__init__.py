import os
from flask import Flask
from config import Config
from app.extensions import db, login_manager, csrf, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from app.blueprints.main import main_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.admin import admin_bp
    from app.blueprints.payment import payment_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(payment_bp, url_prefix='/payment')

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_cart_count():
        from flask_login import current_user
        from flask import session
        count = 0
        if current_user.is_authenticated:
            from app.models import CartItem
            count = CartItem.query.filter_by(user_id=current_user.id).count()
        elif 'cart' in session:
            count = len(session['cart'])
        return dict(cart_count=count)

    @app.context_processor
    def inject_categories():
        from app.models import Category
        categories = Category.query.filter_by(is_active=True).all()
        return dict(nav_categories=categories)

    # Only create tables in development or when explicitly requested
    if not os.environ.get('VERCEL') and not os.environ.get('FLASK_ENV') == 'production':
        with app.app_context():
            try:
                db.create_all()
            except Exception as e:
                print(f"Warning: Could not create database tables: {e}")

    return app
