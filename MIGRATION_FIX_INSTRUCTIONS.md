# Clear all migration history and create fresh ones
# This file contains instructions for fixing migration conflicts

## Step 1: Backup current migrations (optional)
# mkdir migrations_backup
# cp TGConnect/migrations/*.py migrations_backup/

## Step 2: Reset migrations
# Remove all migration files except __init__.py
# Keep only: TGConnect/migrations/__init__.py

## Step 3: Create fresh migrations
# python manage.py makemigrations TGConnect

## Step 4: Apply migrations
# python manage.py migrate

## For Render deployment:
# 1. Delete old database from Render dashboard
# 2. Create new PostgreSQL database  
# 3. Update DATABASE_URL environment variable
# 4. Deploy with fresh migrations
