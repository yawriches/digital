#!/usr/bin/env python3
"""
Vercel API Entry Point for Smart Watches E-commerce Platform
This file handles all requests in Vercel's serverless environment.
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set environment variables for Vercel
os.environ['VERCEL'] = '1'
os.environ['FLASK_ENV'] = 'production'

from app import create_app

# Create the Flask application instance
app = create_app()

# This is the WSGI application that Vercel will use
application = app

# For Vercel Python runtime
def handler(request, context):
    """Simple Vercel handler"""
    return app
