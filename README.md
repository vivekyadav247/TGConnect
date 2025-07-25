# TGConnect - Student Management System

A Django-based web application for managing student registrations, attendance, assignments, and academic records.

## Features

- **Student Registration & Management**
- **Teacher/Admin Dashboard**
- **Attendance Management System**
- **Assignment Upload & Verification**
- **Notes & Timetable Management**
- **Email Verification System**
- **Secure Authentication**

## Tech Stack

- **Backend**: Django 5.2.1
- **Database**: SQLite3
- **Frontend**: HTML, CSS, JavaScript
- **Email**: Gmail SMTP
- **Deployment**: Render

## Quick Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables in `.env`
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`

## Environment Variables

```
SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEBUG=True
ALLOWED_HOSTS=your-domain.com,localhost
```

## Deployment

The application is configured for deployment on Render platform with automatic builds from the main branch.

---
*Developed by Vivek Yadav*