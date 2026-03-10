#!/usr/bin/env python3
"""
Test Supabase PostgreSQL connection
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Get the database URL from environment
database_url = os.environ.get('DATABASE_URL')
print(f"Attempting to connect to: {database_url}")

try:
    # Try to connect to Supabase PostgreSQL
    conn = psycopg2.connect(database_url)
    print("✅ Successfully connected to Supabase PostgreSQL!")
    
    # Test a simple query
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"PostgreSQL version: {version[0]}")
    
    cursor.close()
    conn.close()
    print("✅ Connection test completed successfully!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTroubleshooting suggestions:")
    print("1. Check if your internet connection is working")
    print("2. Verify the Supabase project is active")
    print("3. Check if the database URL is correct")
    print("4. Ensure the password is properly URL-encoded")
