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
            "vivekyad240706@gmail.com",  # Replace with your sender email
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

def studenthome(request):
    try:
        sname = request.session.get("sname")
        senroll = request.session.get("senroll")
        
        if not sname or not senroll:
            return redirect("/login/")
            
        return render(request, "studenthome.html", {
            "sname": sname,
            "senroll": senroll
        })
    except Exception as e:
        print(f"Error in studenthome: {e}")
        return redirect("/login/")

def tghome(request):
    try:
        tname = request.session.get("tname")
        tid = request.session.get("tid")
        
        if not tname or not tid:
            return redirect("/logintg/")
            
        return render(request, "tghome.html", {
            "tname": tname,
            "tid": tid
        })
    except Exception as e:
        print(f"Error in tghome: {e}")
        return redirect("/logintg/")

def managestudent(request):
    try:
        tdepartment = request.session.get("tdepartment")
        tname = request.session.get("tname")
        
        if not tdepartment or not tname:
            return redirect("/logintg/")
        
        # Use dynamic department instead of hardcoded "CSE"
        studentdet = models.Register.objects.filter(role="student", branch=tdepartment, status=1).order_by('name')
        
        return render(request, "managestudent.html", {
            "studentdet": studentdet,
            "tname": tname
        })
    except Exception as e:
        print(f"Error in managestudent: {e}")
        return render(request, "error.html", {"message": "Error loading student data."})

def managestudentstatus(request):
    try:
        # Check if TG is logged in
        if not request.session.get("tname"):
            return redirect("/logintg/")
            
        s = request.GET.get("s")
        enroll = request.GET.get("enroll")
        
        if not s or not enroll:
            return redirect("/managestudent/")

        if s == "active":
            models.Register.objects.filter(enroll=enroll).update(status=1)
        elif s == "inactive":
            models.Register.objects.filter(enroll=enroll).update(status=0)
        elif s == "delete":
            models.Register.objects.filter(enroll=enroll).delete()

        return redirect("/managestudent/")
    except Exception as e:
        print(f"Error in managestudentstatus: {e}")
        return redirect("/managestudent/")

def addreports(request):
    try:
        department = request.session.get("tdepartment")
        tname = request.session.get("tname")
        
        if not department or not tname:
            return redirect("/logintg/")
            
        data = models.addreports.objects.filter(branch=department)

        if request.method == "GET":
            return render(request, "addreports.html", {
                "tname": tname,
                "output": "",
                "data": data
            })
        else:
            enroll = request.POST.get("enroll")
            name = request.POST.get("name")
            branch = request.POST.get("branch")
            sem = request.POST.get("sem")
            cgpa = request.POST.get("cgpa")
            
            if not all([enroll, name, branch, sem, cgpa]):
                return render(request, "addreports.html", {
                    "tname": tname,
                    "output": "All fields are required!",
                    "data": data
                })

            if "file" not in request.FILES:
                return render(request, "addreports.html", {
                    "tname": tname,
                    "output": "Please select a file!",
                    "data": data
                })

            file = request.FILES["file"]
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)

            p = models.addreports(
                enroll=enroll, 
                name=name, 
                branch=branch, 
                cgpa=cgpa, 
                sem=sem, 
                filename=filename, 
                info=time.asctime()
            )
            p.save()

            data = models.addreports.objects.filter(branch=branch)
            return render(request, "addreports.html", {
                "tname": tname,
                "output": "Report uploaded successfully!",
                "data": data
            })
    except Exception as e:
        print(f"Error in addreports: {e}")
        return render(request, "error.html", {"message": "Error uploading report. Please try again."})

def viewreports(request):
    try:
        enroll = request.session.get("senroll")
        sname = request.session.get("sname")
        
        if not enroll or not sname:
            return redirect("/login/")
            
        data = models.addreports.objects.filter(enroll=enroll)
        return render(request, "viewreports.html", {
            "sname": sname,
            "data": data
        })
    except Exception as e:
        print(f"Error in viewreports: {e}")
        return render(request, "error.html", {"message": "Error loading reports."})

def managereports(request):
    try:
        if not request.session.get("tname"):
            return redirect("/logintg/")
            
        s = request.GET.get("s")
        enroll = request.GET.get("enroll")
        
        if s == "delete" and enroll:
            models.addreports.objects.filter(enroll=enroll).delete()

        return redirect("/addreports/")
    except Exception as e:
        print(f"Error in managereports: {e}")
        return redirect("/addreports/")

def editTT(request):
    try:
        department = request.session.get("tdepartment")
        tname = request.session.get("tname")
        
        if not department or not tname:
            return redirect("/logintg/")
            
        months = "January February March April May June July August September October November December".split()

        if request.method == "GET":
            data = models.TimeTable.objects.filter(department=department)
            return render(request, "editTT.html", {
                "tname": tname,
                "data": data,
                "months": months,
            })
        else:
            month = request.POST.get("month")
            week = request.POST.get("week")
            fromdate = request.POST.get("fromdate")
            todate = request.POST.get("todate")
            department_post = request.POST.get("department")
            
            if not all([month, week, fromdate, todate, department_post]):
                data = models.TimeTable.objects.filter(department=department)
                return render(request, "editTT.html", {
                    "tname": tname,
                    "data": data,
                    "months": months,
                    "error": "All fields are required!"
                })

            if "file" not in request.FILES:
                data = models.TimeTable.objects.filter(department=department)
                return render(request, "editTT.html", {
                    "tname": tname,
                    "data": data,
                    "months": months,
                    "error": "Please select a file!"
                })

            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)

            p = models.TimeTable(
                department=department_post,
                month=month,
                week=week,
                fromdate=fromdate,
                todate=todate,
                filename=filename,
                info=time.asctime()
            )
            p.save()

            data = models.TimeTable.objects.filter(department=department)
            return render(request, "editTT.html", {
                "tname": tname,
                "data": data,
                "months": months,
                "success": "Timetable uploaded successfully!"
            })
    except Exception as e:
        print(f"Error in editTT: {e}")
        return render(request, "error.html", {"message": "Error managing timetable."})

def manageTT(request):
    try:
        if not request.session.get("tname"):
            return redirect("/logintg/")
            
        s = request.GET.get("s")
        week = request.GET.get("week")
        month = request.GET.get("month")
        department = request.GET.get("department")
        
        if s == "delete" and all([week, month, department]):
            models.TimeTable.objects.filter(
                week=week, 
                month=month, 
                department=department
            ).delete()

        return redirect("/editTT/")
    except Exception as e:
        print(f"Error in manageTT: {e}")
        return redirect("/editTT/")
        
def viewTT(request):
    try:
        department = request.session.get("sbranch")
        sname = request.session.get("sname")
        
        if not department or not sname:
            return redirect("/login/")
            
        data = models.TimeTable.objects.filter(department=department)
        return render(request, "viewTT.html", {
            "sname": sname,
            "data": data
        })
    except Exception as e:
        print(f"Error in viewTT: {e}")
        return render(request, "error.html", {"message": "Error loading timetable."})

def addnotes(request):
    try:
        department = request.session.get("tdepartment")
        tname = request.session.get("tname")
        
        if not department or not tname:
            return redirect("/logintg/")
            
        if request.method == "GET":
            data = models.Notes.objects.filter(department=department)
            return render(request, "addnotes.html", {
                "tname": tname,
                "data": data
            })
        else:
            department_post = request.POST.get("department")
            subject = request.POST.get("subject")
            title = request.POST.get("title")
            
            if not all([department_post, subject, title]):
                data = models.Notes.objects.filter(department=department)
                return render(request, "addnotes.html", {
                    "tname": tname,
                    "data": data,
                    "error": "All fields are required!"
                })

            if "file" not in request.FILES:
                data = models.Notes.objects.filter(department=department)
                return render(request, "addnotes.html", {
                    "tname": tname,
                    "data": data,
                    "error": "Please select a file!"
                })

            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)

            p = models.Notes(
                department=department_post,
                subject=subject,
                title=title,
                filename=filename,
                info=time.asctime()
            )
            p.save()
            
            data = models.Notes.objects.filter(department=department)
            return render(request, "addnotes.html", {
                "tname": tname,
                "data": data,
                "success": "Notes uploaded successfully!"
            })
    except Exception as e:
        print(f"Error in addnotes: {e}")
        return render(request, "error.html", {"message": "Error uploading notes."})
    
def managenotes(request):
    try:
        if not request.session.get("tname"):
            return redirect("/logintg/")
            
        s = request.GET.get("s")
        subject = request.GET.get("subject")
        title = request.GET.get("title")
        department = request.GET.get("department")
        
        if s == "delete" and all([subject, title, department]):
            models.Notes.objects.filter(
                subject=subject,
                title=title,
                department=department
            ).delete()

        return redirect("/addnotes/")
    except Exception as e:
        print(f"Error in managenotes: {e}")
        return redirect("/addnotes/")

def viewnotes(request):
    try:
        department = request.session.get("sbranch")
        sname = request.session.get("sname")
        
        if not department:
            return redirect("/login/")
            
        data = models.Notes.objects.filter(department=department)
        return render(request, "viewnotes.html", {
            "data": data,
            "sname": sname
        })
    except Exception as e:
        print(f"Error in viewnotes: {e}")
        return render(request, "error.html", {"message": "Error loading notes."})

def uploadassign(request):
    try:
        enroll = request.session.get("senroll")
        sname = request.session.get("sname")
        sbranch = request.session.get("sbranch")
        
        if not all([enroll, sname, sbranch]):
            return redirect("/login/")
            
        data = models.UploadAssignment.objects.filter(enroll=enroll)
        
        if request.method == "GET":
            return render(request, "uploadassign.html", {
                "sname": sname,
                "data": data
            })
        else:
            subject = request.POST.get("subject")
            
            if not subject:
                return render(request, "uploadassign.html", {
                    "sname": sname,
                    "data": data,
                    "error": "Subject is required!"
                })

            if "file" not in request.FILES:
                return render(request, "uploadassign.html", {
                    "sname": sname,
                    "data": data,
                    "error": "Please select a file!"
                })

            file = request.FILES["file"]
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)

            p = models.UploadAssignment(
                enroll=enroll,
                name=sname,
                branch=sbranch,
                subject=subject,
                filename=filename,
                verify=0,
                info=time.asctime()
            )
            p.save()

            data = models.UploadAssignment.objects.filter(enroll=enroll)
            return render(request, "uploadassign.html", {
                "data": data,
                "sname": sname,
                "success": "Assignment uploaded successfully!"
            })
    except Exception as e:
        print(f"Error in uploadassign: {e}")
        return render(request, "error.html", {"message": "Error uploading assignment."})
        
def verifyassign(request):
    try:
        branch = request.session.get("tdepartment")
        tname = request.session.get("tname")
        
        if not branch or not tname:
            return redirect("/logintg/")
            
        data = models.UploadAssignment.objects.filter(branch=branch)
        return render(request, "verifyassign.html", {
            "tname": tname,
            "data": data
        })
    except Exception as e:
        print(f"Error in verifyassign: {e}")
        return render(request, "error.html", {"message": "Error loading assignments."})

def verify(request):
    try:
        if not request.session.get("tname"):
            return redirect("/logintg/")
            
        v = request.GET.get("v")
        enroll = request.GET.get("enroll")
        
        if v and enroll:
            if v == "0":
                models.UploadAssignment.objects.filter(enroll=enroll).update(verify=1)
            else:
                models.UploadAssignment.objects.filter(enroll=enroll).update(verify=0)

        return redirect("/verifyassign/")
    except Exception as e:
        print(f"Error in verify: {e}")
        return redirect("/verifyassign/")

def attendance(request):
    try:
        department = request.session.get("tdepartment")
        tg_id = request.session.get("tid")
        
        # Check if TG is logged in
        if not tg_id or not department:
            return redirect("/logintg/")
        
        students = models.Register.objects.filter(branch=department, role="student", status=1).order_by('name')

        today_date = datetime.now().date().strftime("%Y-%m-%d")

        if request.method == "POST":
            attendance_date = request.POST.get("attendance_date")
            if not attendance_date:
                return render(request, "attendance.html", {
                    "students": students,
                    "year": datetime.now().year,
                    "today_date": today_date,
                    "error": "Please select a valid date."
                })
            
            try:
                attendance_date_obj = datetime.strptime(attendance_date, "%Y-%m-%d").date()
            except ValueError:
                return render(request, "attendance.html", {
                    "students": students,
                    "year": datetime.now().year,
                    "today_date": today_date,
                    "error": "Invalid date format."
                })

            for student in students:
                status = request.POST.get(f'attendance_{student.enroll}')
                if status:
                    # Delete existing attendance for this date
                    models.Attendance.objects.filter(
                        enroll=student.enroll, 
                        date=attendance_date_obj, 
                        tg_id=tg_id
                    ).delete()
                    
                    # Create new attendance record
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
    
    except Exception as e:
        print(f"Error in attendance function: {e}")
        return render(request, "error.html", {"message": "Error processing attendance. Please try again."})

def view_attendance(request):
    try:
        tgid = request.session.get("tid")
        department = request.session.get("tdepartment")
        
        # Check if TG is logged in
        if not tgid or not department:
            return redirect("/logintg/")
        
        students = models.Register.objects.filter(branch=department, role="student", status=1)

        today_date = datetime.now().date()
        from_date = request.GET.get("from_date") or "2025-06-01"
        to_date = request.GET.get("to_date") or today_date.strftime("%Y-%m-%d")

        search = request.GET.get("search") or ""

        try:
            from_dt = datetime.strptime(from_date, "%Y-%m-%d").date()
            to_dt = datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            # If date parsing fails, use default dates
            from_dt = datetime.strptime("2025-06-01", "%Y-%m-%d").date()
            to_dt = today_date

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
    
    except Exception as e:
        # Log the error and return a user-friendly error page
        print(f"Error in view_attendance: {e}")
        return render(request, "error.html", {"message": "Error loading attendance data. Please try again."})


def student_view_attendance(request):
    try:
        enroll = request.session.get("senroll")
        sname = request.session.get("sname")
        
        if not enroll:
            return redirect('/login/')
        
        student = models.Register.objects.filter(enroll=enroll, role="student", status=1).first()
        
        if not student:
            return render(request, "error.html", {"message": "Student not found or inactive."})

        default_from_date = date(2025, 6, 1) 
        default_to_date = date.today()

        from_date = request.GET.get("from_date") or default_from_date.strftime("%Y-%m-%d")
        to_date = request.GET.get("to_date") or default_to_date.strftime("%Y-%m-%d")

        try:
            from_dt = datetime.strptime(from_date, "%Y-%m-%d").date()
            to_dt = datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            from_dt = default_from_date
            to_dt = default_to_date

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
            "sname": sname,
        })
    except Exception as e:
        print(f"Error in student_view_attendance: {e}")
        return render(request, "error.html", {"message": "Error loading attendance data."})

def notify(request):
    try:
        user_department = request.session.get("tdepartment")
        tname = request.session.get("tname")
        
        if not user_department or not tname:
            return redirect("/logintg/")
            
        departments = ["CSE", "IT", "CSE-AI", "CSE-DS", "Mechanical", "Electrical", "Civil"]

        if request.method == "GET":
            data = models.Notification.objects.filter(department=user_department)
            return render(request, "notify.html", {
                "tname": tname,
                "departments": departments,
                "data": data,
                "user_department": user_department,
            })
        else:
            title = request.POST.get("title")
            department = request.POST.get("department")
            expiry_date = request.POST.get("expiry_date")
            
            if not all([title, department, expiry_date]):
                data = models.Notification.objects.filter(department=user_department)
                return render(request, "notify.html", {
                    "tname": tname,
                    "departments": departments,
                    "data": data,
                    "user_department": user_department,
                    "error": "All fields are required!"
                })

            if "file" not in request.FILES:
                data = models.Notification.objects.filter(department=user_department)
                return render(request, "notify.html", {
                    "tname": tname,
                    "departments": departments,
                    "data": data,
                    "user_department": user_department,
                    "error": "Please select a file!"
                })

            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)

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
                "tname": tname,
                "departments": departments,
                "data": data,
                "user_department": user_department,
                "success": "Notification uploaded successfully!"
            })
    except Exception as e:
        print(f"Error in notify: {e}")
        return render(request, "error.html", {"message": "Error uploading notification."})

def student_notifications(request):
    try:
        user_department = request.session.get("sbranch")
        sname = request.session.get("sname")
        
        if not user_department:
            return redirect("/login/")

        notifications = models.Notification.objects.filter(
            department=user_department
        ).order_by('-expiry_date')

        today = date.today()

        return render(request, "student_notifications.html", {
            "notifications": notifications,
            "today": today,
            "user_department": user_department,
            "sname": sname,
        })
    except Exception as e:
        print(f"Error in student_notifications: {e}")
        return render(request, "error.html", {"message": "Error loading notifications."})

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

