#!/usr/bin/env bash
# Render build script for Smart Watches E-commerce

set -o errexit

pip install -r requirements.txt

# Create database tables
python -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); db.create_all(); print('Database tables created successfully')"
