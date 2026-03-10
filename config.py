import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database Configuration with fallback
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///smartwatches.db')
    
    # Check if we can use PostgreSQL, fallback to SQLite if connection fails
    if database_url.startswith('postgresql://'):
        try:
            import psycopg2
            # Test connection
            test_conn = psycopg2.connect(database_url)
            test_conn.close()
            SQLALCHEMY_DATABASE_URI = database_url
            print("✅ Using Supabase PostgreSQL database")
        except Exception as e:
            print(f"⚠️  Supabase connection failed: {e}")
            print("🔄 Falling back to SQLite database")
            SQLALCHEMY_DATABASE_URI = 'sqlite:///smartwatches.db'
    else:
        SQLALCHEMY_DATABASE_URI = database_url
        print("📁 Using SQLite database")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY', '')
    PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY', '')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # Supabase Configuration
    SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
    SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY', '')
    SUPABASE_SERVICE_ROLE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY', '')
