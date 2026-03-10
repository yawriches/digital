import os
from flask import Flask
from config import Config
from app.extensions import db, login_manager, csrf


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Create upload folder only if filesystem is writable
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError:
        pass

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

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
        try:
            if current_user.is_authenticated:
                from app.models import CartItem
                count = CartItem.query.filter_by(user_id=current_user.id).count()
            elif 'cart' in session:
                count = len(session['cart'])
        except Exception:
            pass
        return dict(cart_count=count)

    @app.context_processor
    def inject_categories():
        try:
            from app.models import Category
            categories = Category.query.filter_by(is_active=True).all()
            return dict(nav_categories=categories)
        except Exception:
            return dict(nav_categories=[])

    # Create tables only in local development
    if not os.environ.get('VERCEL'):
        with app.app_context():
            try:
                db.create_all()
            except Exception:
                pass

    return app
