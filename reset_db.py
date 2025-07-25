# Reset script for fixing database issues
# Run this to reset migrations and fix database schema

import os
import sys

def reset_database():
    print("Starting database reset process...")
    
    # Reset migrations for TGConnect app
    os.system("python manage.py migrate TGConnect zero")
    
    # Remove migration files (except __init__.py)
    migration_files = [
        "0001_initial.py",
        "0002_addreports_alter_register_email_and_more.py", 
        "0003_register_gender_alter_addreports_sem.py",
        "0004_addreports_branch.py",
        "0005_registertg_alter_register_address_and_more.py",
        "0006_timetable.py",
        "0007_notes_timetable_id_alter_timetable_department.py",
        "0008_alter_notes_title.py",
        "0009_uploadassignment.py",
        "0010_attendance.py",
        "0011_notification.py",
        "0012_alter_addreports_enroll_alter_register_enroll_and_more.py",
        "0013_alter_register_mobile_alter_registertg_department_and_more.py"
    ]
    
    for file in migration_files:
        try:
            os.remove(f"TGConnect/migrations/{file}")
            print(f"Removed {file}")
        except FileNotFoundError:
            print(f"File {file} not found, skipping...")
    
    # Create fresh migrations
    os.system("python manage.py makemigrations")
    
    # Apply migrations
    os.system("python manage.py migrate")
    
    print("Database reset complete!")

if __name__ == "__main__":
    reset_database()
