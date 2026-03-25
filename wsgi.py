import os
import sys

try:
    from app import create_app
    app = create_app()
    
    # Configure WhiteNoise for serving static files in production
    from whitenoise import WhiteNoise
    app.wsgi_app = WhiteNoise(
        app.wsgi_app,
        root=os.path.join(os.path.dirname(__file__), 'app', 'static'),
        prefix='static/'
    )
    
except Exception as e:
    print(f"ERROR creating Flask app: {e}", file=sys.stderr)
    print(f"DATABASE_URL set: {bool(os.environ.get('DATABASE_URL'))}", file=sys.stderr)
    print(f"SECRET_KEY set: {bool(os.environ.get('SECRET_KEY'))}", file=sys.stderr)
    raise

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
