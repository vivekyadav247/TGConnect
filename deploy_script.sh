#!/bin/bash
# Simple deployment script for Render

echo "🚀 Starting TGConnect deployment..."

# Install dependencies
pip install -r requirements.txt

# Create fresh database tables (ignore migration conflicts)
python manage.py migrate --run-syncdb

# Collect static files
python manage.py collectstatic --noinput

echo "✅ Deployment complete!"
