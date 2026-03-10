#!/usr/bin/env python3
"""
Simplified Flask app for Vercel deployment
"""

import os
import sys
from flask import Flask, render_template, request, redirect, url_for

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set environment for Vercel
os.environ['VERCEL'] = '1'
os.environ['FLASK_ENV'] = 'production'

app = Flask(__name__, 
           template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app', 'templates'),
           static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app', 'static'))

# Basic configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-smartwatches-2026')

@app.route('/')
def index():
    """Homepage route"""
    try:
        return render_template('main/index.html')
    except Exception as e:
        return f"""
        <h1>Smart Watches E-commerce</h1>
        <p>Welcome to our premium smart watch collection!</p>
        <p>Template error: {str(e)}</p>
        <p><a href="/debug">Debug Info</a></p>
        """

@app.route('/debug')
def debug():
    """Debug information"""
    return f"""
    <h1>Debug Information</h1>
    <p>App working: ✅</p>
    <p>Template folder: {app.template_folder}</p>
    <p>Static folder: {app.static_folder}</p>
    <p>SECRET_KEY set: {'✅' if app.config.get('SECRET_KEY') else '❌'}</p>
    <p>DATABASE_URL: {os.environ.get('DATABASE_URL', 'Not set')[:50]}...</p>
    <p>VERCEL: {os.environ.get('VERCEL', 'Not set')}</p>
    <p>Current directory: {os.getcwd()}</p>
    <p>Python path: {sys.path[:3]}</p>
    """

@app.route('/shop')
def shop():
    """Shop page"""
    return """
    <h1>Shop - Smart Watches</h1>
    <p>Our premium collection will be available soon!</p>
    <p><a href="/">← Back to Home</a></p>
    """

@app.errorhandler(404)
def not_found(error):
    return f"""
    <h1>404 - Page Not Found</h1>
    <p>The page you're looking for doesn't exist.</p>
    <p><a href="/">← Back to Home</a></p>
    """, 404

@app.errorhandler(500)
def internal_error(error):
    return f"""
    <h1>500 - Internal Server Error</h1>
    <p>Something went wrong: {str(error)}</p>
    <p><a href="/">← Back to Home</a></p>
    """, 500

# Export for Vercel
application = app
