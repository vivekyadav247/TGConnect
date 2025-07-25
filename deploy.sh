#!/bin/bash
# Deployment script for Render

echo "Starting deployment..."

# Install dependencies
pip install -r requirements.txt

# Reset problematic migrations
python manage.py migrate TGConnect 0006 --fake

# Remove problematic migration file
rm -f TGConnect/migrations/0007_notes_timetable_id_alter_timetable_department.py

# Create fresh migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

echo "Deployment complete!"
