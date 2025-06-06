from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from . import models 
from django.utils.timezone import now
from datetime import datetime , timedelta , date
import time
import random

def welcome(request):
    return render(request,"welcome.html")

def register(request):
    if request.method == "GET":
        return render(request, "register.html", {"output": ""})
    else:
        enroll = request.POST.get("enroll")
        name = request.POST.get("name")
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        course = request.POST.get("course")
        branch = request.POST.get("branch")
        year = request.POST.get("year")
        password = request.POST.get("password")

        # Save in session temporarily
        request.session["temp_register"] = {
            "enroll": enroll,
            "name": name,
            "dob": dob,
            "gender": gender,
            "email": email,
            "mobile": mobile,
            "address": address,
            "course": course,
            "branch": branch,
            "year": year,
            "password": password,
        }

        # Send OTP
        otp = random.randint(100000, 999999)
        request.session["otp"] = str(otp)

        send_mail(
            "Email Verification - TGConnect",
            f"Dear {name},\n\nYour OTP for email verification is: {otp}\n\nThanks,\nTGConnect",
            "noreply@tgconnect.com",
            [email],
            fail_silently=False,
        )

        return redirect("/verifyotp/")

def verifyotp(request):
    if request.method == "GET":
        return render(request, "verifyotp.html", {"msg": ""})
    else:
        entered_otp = request.POST.get("otp")
        real_otp = request.session.get("otp")

        if entered_otp == real_otp:
            data = request.session.get("temp_register")
            if data:
                p = models.Register(
                    enroll=data["enroll"],
                    name=data["name"],
                    dob=data["dob"],
                    gender=data["gender"],
                    email=data["email"],
                    mobile=data["mobile"],
                    address=data["address"],
                    course=data["course"],
                    branch=data["branch"],
                    year=data["year"],
                    password=data["password"],
                    status=1,  # status verified
                    role="student",
                    info=time.asctime()
                )
                p.save()

                # Clear session
                del request.session["temp_register"]
                del request.session["otp"]

                return redirect("/studentsuccess/")
            else:
                return render(request, "verifyotp.html", {"msg": "Session expired. Please register again."})
        else:
            return render(request, "verifyotp.html", {"msg": "Invalid OTP. Try again."})

def studentsuccess(request):
    return render(request,"studentsuccess.html")

def tgsuccess(request):
    return render(request,"tgsuccess.html")

def failed(request):
    return render(request,"failed.html")

def login(request) :
    if request.method=="GET" :
        return render(request,"login.html")
    else :
        enroll = request.POST.get("enroll")
        password = request.POST.get("password")

        studentdet = models.Register.objects.filter(enroll=enroll,password=password,status=1)

        if len(studentdet)>0 :
            request.session['sname'] = studentdet[0].name
            request.session['senroll'] = studentdet[0].enroll
            request.session['sbranch'] = studentdet[0].branch
            request.session['semail'] = studentdet[0].email
            return redirect("/studenthome/")
        else :
            return redirect("/failed/")
        
def forgotpassword(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "reset":
            otp = request.POST.get("otp")
            new_password = request.POST.get("new_password")
            session_otp = request.session.get("reset_otp")
            email = request.session.get("reset_email")

            if otp == session_otp and email:
                user = models.Register.objects.get(email=email)
                user.password = new_password
                user.save()

                del request.session['reset_otp']
                del request.session['reset_email']

                return render(request, "forgotpassword.html", {
                    "success": "Password reset successfully!",
                    "button_action": "",
                    "button_text": ""
                })
            else:
                return redirect('/failedotp/')

        else:
            email = request.POST.get("email", "").strip().lower()
            user = models.Register.objects.filter(email=email).first()

            if user:
                otp = str(random.randint(100000, 999999))
                request.session['reset_email'] = email
                request.session['reset_otp'] = otp

                send_mail(
                    "TGConnect Password Reset OTP",
                    f"Your OTP for password reset is: {otp}",
                    "your_email@gmail.com",
                    [email],
                    fail_silently=False,
                )

                return render(request, "forgotpassword.html", {
                    "msg": "OTP sent to your email.",
                    "show_otp": True,
                    "email": email,
                    "button_action": "reset",
                    "button_text": "Reset Password"
                })
            else:
                return render(request, "forgotpassword.html", {
                    "msg": "Email not registered.",
                    "button_action": "send_otp",
                    "button_text": "Send OTP",
                    "email": email
                })

    else:
        return render(request, "forgotpassword.html", {
            "msg": "",
            "button_action": "send_otp",
            "button_text": "Send OTP"
        })

def failedotp(request):
    return render(request,"failedotp.html")

def registertg(request):
    if request.method == "GET":
        return render(request, "registertg.html")

    else:
        id = request.POST.get("id")
        name = request.POST.get("name")
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        course = request.POST.get("course")
        department = request.POST.get("department")
        year = request.POST.get("year")
        password = request.POST.get("password")

        otp = random.randint(100000, 999999)
        request.session["temp_tg_data"] = {
            "id": id,
            "name": name,
            "dob": dob,
            "gender": gender,
            "email": email,
            "mobile": mobile,
            "course": course,
            "department": department,
            "year": year,
            "password": password,
            "otp": otp
        }

        # Send Email
        send_mail(
            "Verify Your Email for TG Registration",
            f"Your OTP is: {otp}",
            "your-email@example.com",  # Replace with your sender email
            [email],
            fail_silently=False
        )

        return render(request, "verifytg.html", {"email": email})

def verifytg(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        temp_data = request.session.get("temp_tg_data")

        if temp_data and str(temp_data["otp"]) == entered_otp:
            # Save to DB
            p = models.RegisterTG(
                id=temp_data["id"],
                name=temp_data["name"],
                dob=temp_data["dob"],
                gender=temp_data["gender"],
                email=temp_data["email"],
                mobile=temp_data["mobile"],
                course=temp_data["course"],
                department=temp_data["department"],
                year=temp_data["year"],
                password=temp_data["password"],
                status=1,
                role="tg",
                info=time.asctime()
            )
            p.save()
            del request.session["temp_tg_data"]
            return redirect("/tgsuccess/")
        else:
            return render(request, "verifytg.html", {"email": temp_data["email"], "error": "Invalid OTP!"})
    else:
        return redirect("/registertg/")

def logintg(request) :
    if request.method=="GET" :
        return render(request,"logintg.html")
    else :
        id = request.POST.get("id")
        password = request.POST.get("password")

        tgdet = models.RegisterTG.objects.filter(id=id,password=password,status=1)

        if len(tgdet)>0 :
            request.session['tname'] = tgdet[0].name
            request.session['tid'] = tgdet[0].id
            request.session['tdepartment'] = tgdet[0].department
            return redirect("/tghome/")
        else :
            return redirect("/failed/")

def forgotpasswordtg(request):
    if request.method == "POST":
        email = request.POST.get("email").strip().lower()
        tg = models.RegisterTG.objects.filter(email=email).first()

        if tg:
            otp = str(random.randint(100000, 999999))
            request.session['tg_reset_email'] = email
            request.session['tg_reset_otp'] = otp

            send_mail(
                "TGConnect - TG Password Reset",
                f"Your OTP for password reset is: {otp}",
                "your_email@gmail.com",
                [email],
                fail_silently=False,
            )

            return render(request, "forgotpasswordtg.html", {
                "msg": "",
                "show_otp": True,
                "email": email,
                "button_action": "reset",
                "button_text": "Reset Password"
            })

        return render(request, "forgotpasswordtg.html", {
            "msg": "Email not registered",
            "email": email,
            "button_action": "send_otp",
            "button_text": "Send OTP"
        })

    elif request.method == "GET":
        return render(request, "forgotpasswordtg.html", {
            "msg": "",
            "button_action": "send_otp",
            "button_text": "Send OTP"
        })

    # Handle OTP + Password reset
    elif request.POST.get("action") == "reset":
        otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")
        session_otp = request.session.get("tg_reset_otp")
        email = request.session.get("tg_reset_email")

        if otp == session_otp:
            tg = models.RegisterTG.objects.get(email=email)
            tg.password = new_password
            tg.save()

            del request.session['tg_reset_otp']
            del request.session['tg_reset_email']

            return render(request, "forgotpasswordtg.html", {
                "success": "Password reset successfully!",
                "button_action": "",
                "button_text": ""
            })
        else:
            return redirect('/invalidotp/')

def invalidotp(request):
    return render(request,"invalidotp.html")
 
def about(request) :
    return render(request,"about.html")

def contact(request) :
    return render(request,"contact.html")

def studenthome(request) :
    return render(request,"studenthome.html",{"sname": request.session["sname"],"senroll": request.session["senroll"]})

def tghome(request) :
    return render(request,"tghome.html",{"tname": request.session["tname"],"tid": request.session["tid"]})

def managestudent(request) : 
    studentdet = models.Register.objects.filter(role="student",branch="CSE").order_by('name')
    return render(request,"managestudent.html",{"studentdet": studentdet})

def managestudentstatus(request):
    s = request.GET.get("s")
    enroll = request.GET.get("enroll")

    if s=="active" : 
        models.Register.objects.filter(enroll=enroll).update(status=1)
    elif s=="inactive" : 
        models.Register.objects.filter(enroll=enroll).update(status=0)
    else :
        models.Register.objects.filter(enroll=enroll).delete()

    return redirect("/managestudent/")

def addreports(request):
    department = request.session["tdepartment"]
    data = models.addreports.objects.filter(branch=department)  # Use branch or department as per your model

    if request.method == "GET":
        return render(request, "addreports.html", {
            "tname": request.session["tname"],
            "output": "",
            "data": data
        })
    else:
        enroll = request.POST.get("enroll")
        name = request.POST.get("name")
        branch = request.POST.get("branch")
        sem = request.POST.get("sem")
        cgpa = request.POST.get("cgpa")

        file = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        p = models.addreports(enroll=enroll, name=name, branch=branch, cgpa=cgpa, sem=sem, filename=filename, info=time.asctime())
        p.save()

        data = models.addreports.objects.filter(branch=branch)
        return render(request, "addreports.html", {
            "tname": request.session["tname"],
            "output": "Content Upload Successfully !!",
            "data": data
        })

def viewreports(request) :
    enroll = request.session["senroll"]
    data = models.addreports.objects.filter(enroll=enroll)
    return render(request,"viewreports.html",{"sname": request.session["sname"],"data": data})

def managereports(request):
    s = request.GET.get("s")
    enroll = request.GET.get("enroll")
    if s=="delete" :
        models.addreports.objects.filter(enroll=enroll).delete()

    return redirect("/addreports/")

def editTT(request):
    months = "January February March April May June July August September October November December".split()

    if request.method == "GET":
        department = request.session["tdepartment"]
        data = models.TimeTable.objects.filter(department=department)
        return render(
            request,
            "editTT.html",
            {
                "tname": request.session["tname"],
                "data": data,
                "months": months,  # <-- add this
            }
        )
    else:
        month = request.POST.get("month")
        week = request.POST.get("week")
        fromdate = request.POST.get("fromdate")
        todate = request.POST.get("todate")
        department = request.POST.get("department")

        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        p = models.TimeTable(
            department=department,
            month=month,
            week=week,
            fromdate=fromdate,
            todate=todate,
            filename=filename,
            info=time.asctime()
        )
        p.save()

        department = request.session["tdepartment"]
        data = models.TimeTable.objects.filter(department=department)
        return render(
            request,
            "editTT.html",
            {
                "tname": request.session["tname"],
                "data": data,
                "months": months,  # <-- add this here too
            }
        )

def manageTT(request):
    s = request.GET.get("s")
    week = request.GET.get("week")
    month = request.GET.get("month")
    department = request.GET.get("department")
    
    if s=="delete" :
        models.TimeTable.objects.get(week=week,month=month,department=department).delete()

    return redirect("/editTT/")
        
def viewTT(request) :
    department = request.session["sbranch"]
    data = models.TimeTable.objects.filter(department=department)
    return render(request,"viewTT.html",{"sname": request.session["sname"],"data": data})

def addnotes(request) :
    if request.method=="GET":
        department = request.session["tdepartment"]
        data = models.Notes.objects.filter(department=department)
        return render(request,"addnotes.html",{"tname": request.session["tname"],"data": data})
    else : 
        department = request.POST.get("department")
        subject = request.POST.get("subject")
        title = request.POST.get("title")

        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name,file)


        p = models.Notes(department=department,subject=subject,title=title,filename=filename,info = time.asctime())
        p.save() 
        department = request.session["tdepartment"]
        data = models.Notes.objects.filter(department=department)
        return render(request,"addnotes.html",{"tname": request.session["tname"],"data": data})
    
def managenotes(request):
    s = request.GET.get("s")
    subject = request.GET.get("subject")
    title = request.GET.get("title")
    department = request.GET.get("department")
    
    if s=="delete" :
        models.Notes.objects.get(subject=subject,title=title,department=department).delete()

    return redirect("/addnotes/")

def viewnotes(request):
    department = request.session.get("sbranch")
    data = models.Notes.objects.filter(department=department)
    return render(request, "viewnotes.html", {"data": data})

def uploadassign(request):
    enroll = request.session["senroll"]
    data = models.UploadAssignment.objects.filter(enroll=enroll)
    if request.method=="GET":
        return render(request, "uploadassign.html", {
            "sname": request.session["sname"],
            "data": data
        })
    else :
        name = request.session["sname"]
        branch = request.session["sbranch"]

        subject = request.POST.get("subject")

        file = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        p = models.UploadAssignment(enroll=enroll, name=name, branch=branch, subject=subject, filename=filename, verify = 0 , info=time.asctime())
        p.save()

        data = models.UploadAssignment.objects.filter(enroll=enroll)
        return render(request, "uploadassign.html", {"data": data})
        
def verifyassign(request) :
    branch = request.session["tdepartment"]
    data = models.UploadAssignment.objects.filter(branch=branch)
    return render(request,"verifyassign.html",{"tname": request.session["tname"], "data":data})

def verify(request):
    v = request.GET.get("v")
    enroll = request.GET.get("enroll")

    if v=="0" : 
        models.UploadAssignment.objects.filter(enroll=enroll).update(verify=1)
    else :
        models.UploadAssignment.objects.filter(enroll=enroll).update(verify=0)

    return redirect("/verifyassign/")

def attendance(request):
    department = request.session.get("tdepartment")
    tg_id = request.session.get("tid")
    students = models.Register.objects.filter(branch=department, role="student", status=1).order_by('name')

    today_date = datetime.now().date().strftime("%Y-%m-%d")

    if request.method == "POST":
        attendance_date = request.POST.get("attendance_date")
        try:
            attendance_date_obj = datetime.strptime(attendance_date, "%Y-%m-%d").date()
        except:
            return redirect("/tghome/")

        for student in students:
            status = request.POST.get(f'attendance_{student.enroll}')
            if status:
                models.Attendance.objects.filter(enroll=student.enroll, date=attendance_date_obj, tg_id=tg_id).delete()
                models.Attendance.objects.create(
                    enroll=student.enroll,
                    name=student.name,
                    branch=student.branch,
                    date=attendance_date_obj,
                    status=status,
                    tg_id=tg_id
                )

        return redirect("/tghome/")

    return render(request, "attendance.html", {
        "students": students,
        "year": datetime.now().year,
        "today_date": today_date,
    })

def view_attendance(request):
    tgid = request.session.get("tid")
    department = request.session.get("tdepartment")
    students = models.Register.objects.filter(branch=department, role="student", status=1)

    today_date = datetime.now().date()
    from_date = request.GET.get("from_date") or "2025-06-01"
    to_date = request.GET.get("to_date") or today_date.strftime("%Y-%m-%d")

    search = request.GET.get("search")

    from_dt = datetime.strptime(from_date, "%Y-%m-%d")
    to_dt = datetime.strptime(to_date, "%Y-%m-%d")

    attendance_data = []

    for student in students:
        if search:
            search = search.strip()
            if search and search.lower() not in student.name.lower() and search not in student.enroll:
                continue

        records = models.Attendance.objects.filter(
            enroll=student.enroll,
            tg_id=tgid,
            date__range=(from_dt, to_dt)
        )

        total_days = records.count()
        present = records.filter(status="Present").count()
        absent = records.filter(status="Absent").count()
        leave = records.filter(status="Leave").count()
        effective_days = total_days - leave
        percentage = (present / effective_days * 100) if effective_days > 0 else 0

        attendance_data.append({
            "enroll": student.enroll,
            "name": student.name,
            "branch": student.branch,
            "total_days": total_days,
            "present": present,
            "absent": absent,
            "leave": leave,
            "percentage": round(percentage, 2)
        })

    attendance_data.sort(key=lambda x: x['name'].lower())

    return render(request, "view_attendance.html", {
        "attendance_data": attendance_data,
        "from_date": from_date,
        "to_date": to_date,
        "search": search,
        "today_date": today_date,
    })

def student_view_attendance(request):
    enroll = request.session.get("senroll")  # get enrolled student ID
    if not enroll:
        return redirect('/login/')
    
    student = models.Register.objects.filter(enroll=enroll, role="student", status=1).first()
    
    if not student:
        return render(request, "error.html", {"message": "Student not found or inactive."})

    default_from_date = date(2025, 6, 1) 
    default_to_date = date.today()

    from_date = request.GET.get("from_date") or default_from_date.strftime("%Y-%m-%d")
    to_date = request.GET.get("to_date") or default_to_date.strftime("%Y-%m-%d")

    from_dt = datetime.strptime(from_date, "%Y-%m-%d").date()
    to_dt = datetime.strptime(to_date, "%Y-%m-%d").date()

    attendance_records = models.Attendance.objects.filter(
        enroll=enroll,
        date__range=(from_dt, to_dt)
    ).order_by("date")

    total_days = attendance_records.count()
    present = attendance_records.filter(status="Present").count()
    absent = attendance_records.filter(status="Absent").count()
    leave = attendance_records.filter(status="Leave").count()

    effective_days = total_days - leave
    percentage = (present / effective_days * 100) if effective_days > 0 else 0


    return render(request, "student_view_attendance.html", {
        "student": student,
        "records": attendance_records,
        "from_date": from_date,
        "to_date": to_date,
        "total_days": total_days,
        "present": present,
        "absent": absent,
        "leave": leave,
        "percentage": round(percentage, 2),
    })

def notify(request):
    # List of departments
    departments = ["CSE", "IT", "CSE-AI", "CSE-DS", "Mechanical", "Electrical", "Civil"]

    user_department = request.session.get("tdepartment")  # Teacher's dept from session

    if request.method == "GET":
        # Filter notifications by tg's department only
        data = models.Notification.objects.filter(department=user_department)
        return render(request, "notify.html", {
            "tname": request.session.get("tname"),
            "departments": departments,
            "data": data,
            "user_department": user_department,
        })

    else:
        title = request.POST.get("title")
        department = request.POST.get("department")
        expiry_date = request.POST.get("expiry_date")
        file = request.FILES['file']

        # Save file
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)

        # Save notification
        n = models.Notification(
            department=department,
            title=title,
            notice_file=filename,
            info=time.asctime(),
            expiry_date=expiry_date
        )
        n.save()

        data = models.Notification.objects.filter(department=user_department)
        return render(request, "notify.html", {
            "tname": request.session.get("tname"),
            "departments": departments,
            "data": data,
            "user_department": user_department,
        })

def student_notifications(request):
    user_department = request.session.get("sbranch") 

    notifications = models.Notification.objects.filter(department=user_department).order_by('-expiry_date')

    today = date.today()

    return render(request, "student_notifications.html", {
        "notifications": notifications,
        "today": today,
        "user_department": user_department,
    })

def editprofile(request):
    email = request.session.get("semail")
    if not email:
        return redirect("/login/") 

    user = models.Register.objects.filter(email=email).first()
    if not user:
        return redirect("/login/")

    if request.method == "POST":
        user.name = request.POST.get("name")
        user.dob = request.POST.get("dob")
        user.gender = request.POST.get("gender")
        user.mobile = request.POST.get("mobile")
        user.address = request.POST.get("address")
        user.course = request.POST.get("course")
        user.branch = request.POST.get("branch")
        user.year = request.POST.get("year")

        # Optional password change
        new_password = request.POST.get("password")
        if new_password:
            user.password = new_password

        user.save()
        return render(request, "editprofile.html", {
            "user": user,
            "success": "Profile updated successfully.",
            "branches": ["CSE", "IT", "CSE-AI", "CSE-DS", "Mechanical", "Electrical", "Civil"],
            "years": ["2022-2026", "2023-2027", "2024-2028", "2025-2029"],
            "courses": ["B.Tech", "Diploma"]
        })

    return render(request, "editprofile.html", {
        "user": user,
        "branches": ["CSE", "IT", "CSE-AI", "CSE-DS", "Mechanical", "Electrical", "Civil"],
        "years": ["2022-2026", "2023-2027", "2024-2028", "2025-2029"],
        "courses": ["B.Tech", "Diploma"]
    })

def logout_student(request):
    request.session.flush()
    return redirect("/")

def logout_tg(request):
    request.session.flush()
    return redirect("/")

