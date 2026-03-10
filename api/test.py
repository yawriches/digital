#!/usr/bin/env python3
"""
Minimal Flask app for testing Vercel deployment
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return """
    <h1>🎉 Flask on Vercel Works!</h1>
    <p>This is a minimal test to verify Vercel deployment.</p>
    <p>If you see this, the basic Flask setup is working.</p>
    """

@app.route('/test')
def test():
    import os
    return f"""
    <h1>Environment Test</h1>
    <p>VERCEL: {os.environ.get('VERCEL', 'Not set')}</p>
    <p>DATABASE_URL: {os.environ.get('DATABASE_URL', 'Not set')[:50]}...</p>
    <p>SECRET_KEY: {os.environ.get('SECRET_KEY', 'Not set')[:20]}...</p>
    """

# Export for Vercel
application = app
