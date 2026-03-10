#!/usr/bin/env python3
"""
WSGI Entry Point for Smart Watches E-commerce Platform
This file is used by production WSGI servers like Gunicorn, uWSGI, etc.
"""

from app import create_app

# Create the Flask application instance
application = create_app()

# For compatibility with different WSGI servers
app = application

if __name__ == '__main__':
    application.run()
