#!/usr/bin/env python3
"""
Vercel API Entry Point for Smart Watches E-commerce Platform
This file handles all requests in Vercel's serverless environment.
"""

import sys
import os
from flask import Flask

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Set environment variables for Vercel
os.environ['VERCEL'] = '1'
os.environ['FLASK_ENV'] = 'production'

try:
    from app import create_app
    
    # Create the Flask application instance
    app = create_app()
    
except Exception as e:
    # Fallback minimal Flask app for debugging
    app = Flask(__name__)
    
    @app.route('/')
    def debug_info():
        return f"""
        <h1>Debug Info</h1>
        <p>Error creating app: {str(e)}</p>
        <p>Python path: {sys.path}</p>
        <p>Current directory: {os.getcwd()}</p>
        <p>Files in current dir: {os.listdir('.')}</p>
        <p>Environment variables: {dict(os.environ)}</p>
        """
    
    @app.route('/<path:path>')
    def catch_all(path):
        return f"Path: {path}, Error: {str(e)}"

# Export for Vercel
application = app
