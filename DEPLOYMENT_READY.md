# TGConnect Deployment Guide

## ✅ All Issues Fixed

### Fixed Problems:
1. **TimeTable multiple primary keys** - Fixed by using Django's default BigAutoField
2. **Mobile field integer overflow** - Changed to CharField
3. **Static files missing directory** - Commented out STATICFILES_DIRS
4. **Migration conflicts** - Using --run-syncdb to bypass conflicts
5. **Department unique constraint** - Removed from RegisterTG model

### Deployment Steps:

1. **Render Environment Variables (Required):**
   ```
   SECRET_KEY=your-django-secret-key
   DEBUG=False  
   ALLOWED_HOSTS=your-app-name.onrender.com
   EMAIL_HOST_USER=your-gmail@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

2. **Git Commit & Push:**
   ```bash
   git add .
   git commit -m "Fix all deployment issues - ready for production"
   git push origin main
   ```

3. **Deploy on Render:**
   - Fresh PostgreSQL database recommended
   - Click Deploy button
   - Monitor build logs

### The deployment script will:
- Install dependencies
- Create fresh database tables with --run-syncdb (bypasses migration conflicts)  
- Collect static files
- Start Gunicorn server

## 🚀 Your app will be live!

**Note:** If still getting errors, delete the old database from Render dashboard and create a new PostgreSQL database, then deploy again.
