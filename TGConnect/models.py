from django.db import models

class Register(models.Model) :
    enroll=models.CharField(primary_key=True,unique=True)
    name=models.CharField(max_length=50)
    dob=models.DateField()
    gender = models.CharField()
    email=models.EmailField(unique=True)
    mobile=models.IntegerField(unique=True)
    address = models.CharField(max_length=100)
    course = models.CharField(max_length=20)
    branch = models.CharField(max_length=20)
    year = models.CharField(max_length=20)
    password = models.CharField(max_length=10)
    status = models.IntegerField()
    role = models.CharField(max_length=10)
    info = models.CharField(max_length=50)

class RegisterTG(models.Model) :
    id=models.CharField(primary_key=True,unique=True)
    name=models.CharField(max_length=50)
    dob=models.DateField()
    gender = models.CharField(max_length=10)
    email=models.EmailField(unique=True)
    mobile=models.IntegerField(unique=True)
    course = models.CharField(max_length=20)
    department = models.CharField(max_length=20,unique=True)
    year = models.CharField(max_length=10)
    password = models.CharField(max_length=10)
    status = models.IntegerField(default=0)
    role = models.CharField(max_length=10)
    info = models.CharField(max_length=50)

class addreports(models.Model) :
    enroll=models.CharField(primary_key=True,unique=True)
    name=models.CharField(max_length=50)
    branch = models.CharField(max_length=20)
    sem = models.IntegerField()
    cgpa = models.FloatField()
    filename = models.CharField(max_length=100)
    info = models.CharField(max_length=50)

class TimeTable(models.Model):
    department = models.CharField(max_length=20)
    month = models.CharField(max_length=10)
    week = models.CharField(max_length=10)
    fromdate = models.CharField(max_length=20)
    todate = models.CharField(max_length=20)
    filename = models.CharField(max_length=20)
    info = models.CharField(max_length=50)

class Notes(models.Model) :
    department = models.CharField(max_length=20)
    subject = models.CharField(max_length=20)
    title = models.CharField(max_length=50,unique=True)
    filename = models.CharField(max_length=50)
    info = models.CharField(max_length=50)

class UploadAssignment(models.Model) :
    enroll=models.CharField(primary_key=True,unique=True)
    name=models.CharField(max_length=50)
    branch = models.CharField(max_length=20)
    subject = models.CharField(max_length=25)
    filename = models.CharField(max_length=40)
    verify = models.IntegerField()
    info = models.CharField(max_length=45)

class Attendance(models.Model):
    enroll = models.CharField(max_length=20)     # Student's enrollment number
    name = models.CharField(max_length=100)      # Student's name
    branch = models.CharField(max_length=100)    # Student's branch
    date = models.DateField()                    # Date of attendance
    status = models.CharField(max_length=10)     # 'Present', 'Absent', or 'Leave'
    tg_id = models.CharField(max_length=20)      # ID of TG who submitted


class Notification(models.Model):
    department = models.CharField(max_length=100)   # Added department
    title = models.CharField(max_length=200)
    notice_file = models.FileField(upload_to='notifications/')
    info = models.CharField(max_length=200)
    expiry_date = models.DateField()

    def __str__(self):
        return self.title
