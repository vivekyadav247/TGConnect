
from django.contrib import admin
from django.urls import path


from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.welcome),
    path('studentsuccess/',views.studentsuccess),
    path('tgsuccess/',views.tgsuccess),
    path('failed/',views.failed),
    path('register/',views.register),
    path("verifyotp/", views.verifyotp),
    path('registertg/',views.registertg),
    path("verifytg/", views.verifytg),
    path('login/',views.login),     
    path("forgotpassword/", views.forgotpassword),
    path('failedotp/',views.failedotp),
    path('logintg/',views.logintg),
    path("forgotpasswordtg/", views.forgotpasswordtg),
    path('invalidotp/',views.invalidotp),
    path('about/',views.about), 
    path('contact/',views.contact),  
    path('studenthome/',views.studenthome),   
    path('tghome/',views.tghome),   
    path('managestudent/',views.managestudent),
    path('managestudentstatus/',views.managestudentstatus),
    path('addreports/',views.addreports),
    path('viewreports/',views.viewreports),
    path('managereports/',views.managereports),
    path('editTT/',views.editTT),
    path('manageTT/',views.manageTT),
    path('viewTT/',views.viewTT),
    path('addnotes/',views.addnotes),
    path('managenotes/',views.managenotes),
    path('viewnotes/',views.viewnotes),
    path('uploadassign/',views.uploadassign),
    path('verifyassign/',views.verifyassign),
    path('verify/',views.verify),
    path('attendance/', views.attendance),
    path('attendance/', views.attendance, name='attendance'),
    path('view_attendance/', views.view_attendance),
    path('student_view_attendance/', views.student_view_attendance),
    path('notify/', views.notify, name='notify'),
    path('student_notifications/', views.student_notifications),
    path('editprofile/',views.editprofile),
    path('logout/', views.logout_student),
    path('logouttg/', views.logout_tg),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)