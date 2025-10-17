# 🎓 TGConnect - Complete Student-Teacher Management System

> A modern, full-featured Django web application for educational institutions to manage students, teachers, academic records, and administrative tasks seamlessly.

## 🚀 Live Demo
- **Application**: https://vivekyadav.pythonanywhere.com/
- **Admin Panel**: `/admin/` (Django built-in admin)

## ✨ Key Features

### 👨‍🎓 Student Features
- **Secure Registration** with OTP email verification
- **Profile Management** with complete academic details
- **Attendance Tracking** with detailed statistics
- **Assignment Submission** system
- **View Academic Reports** (CGPA, Semester results)
- **Access Study Materials** (Notes, Timetables)
- **Notification System** for important updates
- **Password Recovery** via email OTP

### 👨‍🏫 Teacher (TG) Features
- **Student Management** - Activate/Deactivate student accounts
- **Attendance Management** - Mark and track student attendance
- **Assignment Verification** - Review and approve student submissions
- **Academic Reports** - Upload and manage student reports
- **Study Materials** - Upload notes and timetables
- **Notification Broadcasting** - Send notices to students
- **Department-wise Management** - Organized by academic departments

### 🔐 Admin Features
- **Django Admin Panel** - Full database management
- **User Management** - Complete control over all accounts
- **System Monitoring** - Track all activities and statistics
- **Content Management** - Manage all academic content
- **Security Controls** - Advanced authentication and permissions

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend Framework** | Django 5.2.1 |
| **Database** | SQLite3 (Development) / PostgreSQL (Production) |
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5.3.0 |
| **Authentication** | Django Auth + Session Management |
| **Email Service** | Gmail SMTP with OTP verification |
| **File Storage** | Django FileSystemStorage |
| **Icons** | Bootstrap Icons 1.10.5 |
| **Deployment** | Render Platform |

## 📋 System Requirements

- Python 3.8+
- Django 5.2.1
- Modern web browser
- Internet connection (for email features)

## 🚀 Quick Start Guide

### 1. Clone Repository
```bash
git clone https://github.com/vivekyadav247/TGConnect.git
cd TGConnect
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create `.env` file in root directory:
```env
SECRET_KEY=your-super-secret-key-here
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Start Development Server
```bash
python manage.py runserver
```

### 8. Access Application
- **Main Application**: http://localhost:8000/
- **Django Admin**: http://localhost:8000/admin/

## 📁 Project Structure

```
TGConnect/
├── TGConnect/                 # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # Application logic
│   ├── urls.py               # URL routing
│   ├── settings.py           # Django configuration
│   ├── templates/            # HTML templates
│   └── static/               # CSS, JS, Images
├── media/                    # User uploaded files
├── staticfiles/              # Collected static files
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management
└── README.md                 # Project documentation
```

## 🎯 Core Functionality

### Registration & Authentication
- **Student Registration**: OTP-verified email registration
- **Teacher Registration**: Department-specific registration
- **Secure Login**: Session-based authentication
- **Password Recovery**: Email OTP reset system
- **Profile Management**: Complete user profile editing

### Academic Management
- **Attendance System**: Date-wise attendance tracking
- **Assignment Management**: Upload, verify, and track assignments
- **Report Management**: CGPA and semester reports
- **Study Materials**: Notes and timetable sharing
- **Notification System**: Department-wise announcements

### Administrative Controls
- **User Activation**: Admin control over account activation
- **Content Management**: Upload and manage academic content
- **System Statistics**: Complete overview of system usage
- **Data Management**: Full CRUD operations via Django admin

## 🔧 Configuration

### Email Configuration (Gmail)
1. Enable 2-Factor Authentication in Gmail
2. Generate App Password
3. Add credentials to `.env` file

### Department Setup
Available departments:
- CSE (Computer Science Engineering)
- IT (Information Technology)
- CSE-AI (Computer Science - Artificial Intelligence)
- CSE-DS (Computer Science - Data Science)
- Mechanical Engineering
- Electrical Engineering
- Civil Engineering

## 🚢 Deployment

### Render Platform
1. Connect GitHub repository
2. Configure environment variables
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python manage.py runserver 0.0.0.0:$PORT`

### Environment Variables for Production
```env
SECRET_KEY=production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.onrender.com
DATABASE_URL=your-database-url
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Manual Testing Checklist
- [ ] Student registration with OTP
- [ ] Teacher registration and login
- [ ] Attendance marking and viewing
- [ ] Assignment upload and verification
- [ ] Email notifications
- [ ] Admin panel access
- [ ] Profile editing
- [ ] Password recovery

## 📊 Database Models

### Core Models
- **Register**: Student information and authentication
- **RegisterTG**: Teacher information and authentication
- **Attendance**: Daily attendance records
- **UploadAssignment**: Student assignment submissions
- **addreports**: Academic reports and CGPA
- **Notes**: Study materials and notes
- **TimeTable**: Class schedules
- **Notification**: System announcements

## 🔐 Security Features

- **CSRF Protection**: Django built-in CSRF middleware
- **Session Security**: Secure session management
- **Input Validation**: Form validation and sanitization
- **Email Verification**: OTP-based email verification
- **Password Security**: Secure password handling
- **Access Control**: Role-based access permissions

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📞 Support & Contact

- **Developed by**: Vivek Yadav
- **Email**: vivekyad240706@gmail.com 
- **GitHub**: [@vivekyadav247](https://github.com/vivekyadav247)
- **Repository**: [TGConnect](https://github.com/vivekyadav247/TGConnect)

## 🎉 Acknowledgments

- Django Framework for robust backend
- Bootstrap for responsive UI
- Render platform for hosting
- Gmail SMTP for email services

---

### 📈 Project Status: **Production Ready** ✅



*Last updated: July 2025*
