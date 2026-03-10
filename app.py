#!/usr/bin/env python3
"""
Flask Application Entry Point for Smart Watches E-commerce Platform
This file serves as the main entry point for deployment platforms.
"""

from app import create_app

# Create the Flask application instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
