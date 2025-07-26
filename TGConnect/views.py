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
import logging

# Set up logging for production
logger = logging.getLogger(__name__)

def welcome(request):
    return render(request,"welcome.html")

def register(request):
    if request.method == "GET":
        return render(request, "register.html", {"output": ""})
    else:
        try:
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

            # Check if all fields are provided
            if not all([enroll, name, dob, gender, email, mobile, address, course, branch, year, password]):
                return render(request, "register.html", {"output": "All fields are required!"})

            # Check if enrollment already exists
            if models.Register.objects.filter(enroll=enroll).exists():
                return render(request, "register.html", {"output": "Enrollment number already exists!"})

            # Check if email already exists
            if models.Register.objects.filter(email=email).exists():
                return render(request, "register.html", {"output": "Email already registered!"})

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
                f"Dear {name},\n\nYour OTP for email verification is: {otp}\n\nPlease verify your email to complete registration.\n\nThanks,\nTGConnect Team",
                "vivekyad240706@gmail.com",
                [email],
                fail_silently=False,
            )

            return redirect("/verifyotp/")
        except Exception as e:
            print(f"Error in register: {e}")
            return render(request, "register.html", {"output": "Registration failed. Please try again."})

def verifyotp(request):
    if request.method == "GET":
        return render(request, "verifyotp.html", {"msg": ""})
    else:
        try:
            entered_otp = request.POST.get("otp")
            real_otp = request.session.get("otp")
            
            if not entered_otp:
                return render(request, "verifyotp.html", {"msg": "Please enter OTP."})

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
                        status=0,  # status verified
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
                return render(request, "verifyotp.html", {"msg": "Invalid OTP. Please try again."})
        except Exception as e:
            print(f"Error in verifyotp: {e}")
            return render(request, "verifyotp.html", {"msg": "Verification failed. Please try again."})

def studentsuccess(request):
    return render(request,"studentsuccess.html")

def tgsuccess(request):
    return render(request,"tgsuccess.html")

def failed(request):
    return render(request,"failed.html")

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        try:
            enroll = request.POST.get("enroll")
            password = request.POST.get("password")
            
            if not enroll or not password:
                return render(request, "login.html", {"error": "Please enter both enrollment and password."})

            studentdet = models.Register.objects.filter(enroll=enroll, password=password, status=1)

            if len(studentdet) > 0:
                request.session['sname'] = studentdet[0].name
                request.session['senroll'] = studentdet[0].enroll
                request.session['sbranch'] = studentdet[0].branch
                request.session['semail'] = studentdet[0].email
                return redirect("/studenthome/")
            else:
                return redirect("/failed/")
        except Exception as e:
            print(f"Error in login: {e}")
            return redirect("/failed/")
        
def forgotpassword(request):
    if request.method == "POST":
        try:
            action = request.POST.get("action")

            if action == "reset":
                otp = request.POST.get("otp")
                new_password = request.POST.get("new_password")
                session_otp = request.session.get("reset_otp")
                email = request.session.get("reset_email")

                if not otp or not new_password:
                    return render(request, "forgotpassword.html", {
                        "msg": "Please enter both OTP and new password.",
                        "show_otp": True,
                        "email": email,
                        "button_action": "reset",
                        "button_text": "Reset Password"
                    })

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
                if not email:
                    return render(request, "forgotpassword.html", {
                        "msg": "Please enter your email address.",
                        "button_action": "send_otp",
                        "button_text": "Send OTP"
                    })

                user = models.Register.objects.filter(email=email).first()

                if user:
                    otp = str(random.randint(100000, 999999))
                    request.session['reset_email'] = email
                    request.session['reset_otp'] = otp

                    send_mail(
                        "TGConnect Password Reset OTP",
                        f"Dear {user.name},\n\nYour OTP for password reset is: {otp}\n\nIf you didn't request this, please ignore this email.\n\nThanks,\nTGConnect Team",
                        "vivekyad240706@gmail.com",
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
        except Exception as e:
            print(f"Error in forgotpassword: {e}")
            return render(request, "forgotpassword.html", {
                "msg": "An error occurred. Please try again.",
                "button_action": "send_otp",
                "button_text": "Send OTP"
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
        try:
            id = request.POST.get("id", "").strip()
            name = request.POST.get("name", "").strip()
            dob = request.POST.get("dob", "").strip()
            gender = request.POST.get("gender", "").strip()
            email = request.POST.get("email", "").strip().lower()
            mobile = request.POST.get("mobile", "").strip()
            course = request.POST.get("course", "").strip()
            department = request.POST.get("department", "").strip()
            year = request.POST.get("year", "").strip()
            password = request.POST.get("password", "").strip()

            # Validate required fields
            if not all([id, name, dob, gender, email, mobile, course, department, year, password]):
                return render(request, "registertg.html", {
                    "error": "All fields are required.",
                    "id": id, "name": name, "dob": dob, "gender": gender,
                    "email": email, "mobile": mobile, "course": course,
                    "department": department, "year": year
                })

            # Check for duplicate registrations
            existing_id = models.RegisterTG.objects.filter(id=id).first()
            if existing_id:
                return render(request, "registertg.html", {
                    "error": "ID already registered.",
                    "name": name, "dob": dob, "gender": gender,
                    "email": email, "mobile": mobile, "course": course,
                    "department": department, "year": year
                })

            existing_email = models.RegisterTG.objects.filter(email=email).first()
            if existing_email:
                return render(request, "registertg.html", {
                    "error": "Email already registered.",
                    "id": id, "name": name, "dob": dob, "gender": gender,
                    "mobile": mobile, "course": course,
                    "department": department, "year": year
                })

            existing_mobile = models.RegisterTG.objects.filter(mobile=mobile).first()
            if existing_mobile:
                return render(request, "registertg.html", {
                    "error": "Mobile number already registered.",
                    "id": id, "name": name, "dob": dob, "gender": gender,
                    "email": email, "course": course,
                    "department": department, "year": year
                })

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
            try:
                send_mail(
                    "Verify Your Email for TG Registration",
                    f"Dear {name},\n\nWelcome to TGConnect! Your OTP for teacher registration is: {otp}\n\nPlease use this OTP to verify your account.\n\nThanks,\nTGConnect Team",
                    "vivekyad240706@gmail.com",
                    [email],
                    fail_silently=False
                )
                print(f"Email sent successfully to {email} with OTP {otp}")
                # If email sent successfully, redirect to verification page
                return redirect("/verifytg/")
            except Exception as email_error:
                print(f"Email sending failed: {email_error}")
                # Clear session data if email fails
                if "temp_tg_data" in request.session:
                    del request.session["temp_tg_data"]
                return render(request, "registertg.html", {
                    "error": "Failed to send verification email. Please check your email address and try again.",
                    "id": id, "name": name, "dob": dob, "gender": gender,
                    "email": email, "mobile": mobile, "course": course,
                    "department": department, "year": year
                })
        except Exception as e:
            print(f"Error in registertg: {e}")
            return render(request, "registertg.html", {
                "error": "An error occurred during registration. Please try again.",
                "id": id if 'id' in locals() else "",
                "name": name if 'name' in locals() else "",
                "dob": dob if 'dob' in locals() else "",
                "gender": gender if 'gender' in locals() else "",
                "email": email if 'email' in locals() else "",
                "mobile": mobile if 'mobile' in locals() else "",
                "course": course if 'course' in locals() else "",
                "department": department if 'department' in locals() else "",
                "year": year if 'year' in locals() else ""
            })

def verifytg(request):
    if request.method == "POST":
        try:
            entered_otp = request.POST.get("otp", "").strip()
            temp_data = request.session.get("temp_tg_data")

            if not entered_otp:
                return render(request, "verifytg.html", {
                    "email": temp_data.get("email", "") if temp_data else "",
                    "error": "Please enter the OTP."
                })

            if not temp_data:
                return render(request, "registertg.html", {
                    "error": "Session expired. Please register again."
                })

            if str(temp_data["otp"]) == entered_otp:
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
                    status=0,
                    role="tg",
                    info=time.asctime()
                )
                p.save()
                del request.session["temp_tg_data"]
                return redirect("/tgsuccess/")
            else:
                return render(request, "verifytg.html", {
                    "email": temp_data["email"],
                    "error": "Invalid OTP!"
                })
        except Exception as e:
            print(f"Error in verifytg: {e}")
            return render(request, "verifytg.html", {
                "error": "An error occurred during verification. Please try again."
            })
    else:
        # GET request - show verification page with email from session
        temp_data = request.session.get("temp_tg_data")
        if temp_data:
            return render(request, "verifytg.html", {"email": temp_data.get("email", "")})
        else:
            return render(request, "registertg.html", {
                "error": "Session expired. Please register again."
            })

def logintg(request):
    """
    Teacher login function - Production ready for Render deployment
    """
    if request.method == "GET":
        return render(request, "logintg.html")
    else:
        try:
            id = request.POST.get("id", "").strip()
            password = request.POST.get("password", "").strip()

            if not id or not password:
                return render(request, "logintg.html", {
                    "error": "Please enter both ID and password."
                })

            # Fetch teacher with error handling
            try:
                tgdet = models.RegisterTG.objects.filter(
                    id=id, 
                    password=password, 
                    status=1
                )
                
                if tgdet.exists():
                    teacher = tgdet.first()
                    
                    # Set session variables safely
                    request.session['tname'] = teacher.name
                    request.session['tid'] = teacher.id
                    request.session['tdepartment'] = teacher.department
                    
                    logger.info(f"Successful TG login: {teacher.id}")
                    return redirect("/tghome/")
                else:
                    logger.warning(f"Failed TG login attempt for ID: {id}")
                    return render(request, "logintg.html", {
                        "error": "Invalid credentials or account inactive."
                    })
                    
            except Exception as db_error:
                logger.error(f"Database error during TG login: {str(db_error)}")
                return render(request, "logintg.html", {
                    "error": "System error. Please try again later."
                })
                
        except Exception as e:
            logger.error(f"Unexpected error in logintg: {str(e)}")
            return render(request, "logintg.html", {
                "error": "An unexpected error occurred. Please try again."
            })

def forgotpasswordtg(request):
    if request.method == "POST":
        try:
            action = request.POST.get("action")

            if action == "reset":
                otp = request.POST.get("otp", "").strip()
                new_password = request.POST.get("new_password", "").strip()
                session_otp = request.session.get("tg_reset_otp")
                email = request.session.get("tg_reset_email")

                if not otp or not new_password:
                    return render(request, "forgotpasswordtg.html", {
                        "msg": "Please enter both OTP and new password.",
                        "show_otp": True,
                        "email": email,
                        "button_action": "reset",
                        "button_text": "Reset Password"
                    })

                if otp == session_otp and email:
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

            else:
                email = request.POST.get("email", "").strip().lower()
                if not email:
                    return render(request, "forgotpasswordtg.html", {
                        "msg": "Please enter your email address.",
                        "button_action": "send_otp",
                        "button_text": "Send OTP"
                    })

                tg = models.RegisterTG.objects.filter(email=email).first()

                if tg:
                    otp = str(random.randint(100000, 999999))
                    request.session['tg_reset_email'] = email
                    request.session['tg_reset_otp'] = otp

                    send_mail(
                        "TGConnect - TG Password Reset",
                        f"Dear {tg.name},\n\nYour OTP for password reset is: {otp}\n\nIf you didn't request this, please ignore this email.\n\nThanks,\nTGConnect Team",
                        "vivekyad240706@gmail.com",
                        [email],
                        fail_silently=False,
                    )

                    return render(request, "forgotpasswordtg.html", {
                        "msg": "OTP sent to your email.",
                        "show_otp": True,
                        "email": email,
                        "button_action": "reset",
                        "button_text": "Reset Password"
                    })
                else:
                    return render(request, "forgotpasswordtg.html", {
                        "msg": "Email not registered.",
                        "email": email,
                        "button_action": "send_otp",
                        "button_text": "Send OTP"
                    })
        except Exception as e:
            print(f"Error in forgotpasswordtg: {e}")
            return render(request, "forgotpasswordtg.html", {
                "msg": "An error occurred. Please try again.",
                "button_action": "send_otp",
                "button_text": "Send OTP"
            })

    elif request.method == "GET":
        return render(request, "forgotpasswordtg.html", {
            "msg": "",
            "button_action": "send_otp",
            "button_text": "Send OTP"
        })

def invalidotp(request):
    return render(request,"invalidotp.html")
 
def about(request) :
    return render(request,"about.html")

def contact(request) :
    return render(request,"contact.html")

def studenthome(request):
    """
    Student home page - Production ready for Render deployment
    """
    try:
        sname = request.session.get("sname")
        senroll = request.session.get("senroll")
        
        if not sname or not senroll:
            logger.warning("Unauthorized student home access attempt")
            return redirect("/login/")
        
        # Verify student still exists and is active
        try:
            student = models.Register.objects.get(
                enroll=senroll, 
                role="student", 
                status=1
            )
        except models.Register.DoesNotExist:
            logger.warning(f"Student {senroll} not found or inactive")
            request.session.flush()
            return redirect("/login/")
        except Exception as db_error:
            logger.error(f"Database error verifying student {senroll}: {str(db_error)}")
            return render(request, "error.html", {
                "message": "System error. Please try logging in again."
            })
            
        return render(request, "studenthome.html", {
            "sname": sname,
            "senroll": senroll
        })
        
    except Exception as e:
        logger.error(f"Unexpected error in studenthome: {str(e)}")
        return redirect("/login/")

def tghome(request):
    """
    Teacher home page - Production ready for Render deployment
    """
    try:
        tname = request.session.get("tname")
        tid = request.session.get("tid")
        
        if not tname or not tid:
            logger.warning("Unauthorized TG home access attempt")
            return redirect("/logintg/")
        
        # Verify teacher still exists and is active
        try:
            teacher = models.RegisterTG.objects.get(
                id=tid, 
                role="tg", 
                status=1
            )
        except models.RegisterTG.DoesNotExist:
            logger.warning(f"Teacher {tid} not found or inactive")
            request.session.flush()
            return redirect("/logintg/")
        except Exception as db_error:
            logger.error(f"Database error verifying teacher {tid}: {str(db_error)}")
            return render(request, "error.html", {
                "message": "System error. Please try logging in again."
            })
            
        return render(request, "tghome.html", {
            "tname": tname,
            "tid": tid
        })
        
    except Exception as e:
        logger.error(f"Unexpected error in tghome: {str(e)}")
        return redirect("/logintg/")

def managestudent(request):
    try:
        tdepartment = request.session.get("tdepartment")
        tname = request.session.get("tname")
        
        if not tdepartment or not tname:
            return redirect("/logintg/")
        
        # Show all students (both active and inactive) for management
        studentdet = models.Register.objects.filter(role="student", branch=tdepartment).order_by('name')
        
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
    """
    Teacher attendance marking function - Production ready for Render deployment
    """
    try:
        # Session validation
        department = request.session.get("tdepartment")
        tg_id = request.session.get("tid")
        
        if not tg_id or not department:
            logger.warning("Unauthorized attendance access attempt")
            return redirect("/logintg/")
        
        # Fetch students safely
        try:
            students = models.Register.objects.filter(
                branch=department, 
                role="student", 
                status=1
            ).order_by('name')
            
            if not students.exists():
                return render(request, "attendance.html", {
                    "students": [],
                    "year": datetime.now().year,
                    "today_date": datetime.now().date().strftime("%Y-%m-%d"),
                    "message": "No active students found in your department."
                })
                
        except Exception as db_error:
            logger.error(f"Error fetching students for attendance: {str(db_error)}")
            return render(request, "error.html", {
                "message": "Error loading student data. Please try again."
            })

        today_date = datetime.now().date().strftime("%Y-%m-%d")

        if request.method == "POST":
            attendance_date = request.POST.get("attendance_date", "").strip()
            
            if not attendance_date:
                return render(request, "attendance.html", {
                    "students": students,
                    "year": datetime.now().year,
                    "today_date": today_date,
                    "error": "Please select a valid date."
                })
            
            # Validate date format
            try:
                attendance_date_obj = datetime.strptime(attendance_date, "%Y-%m-%d").date()
                
                # Check if date is not too far in future
                if attendance_date_obj > datetime.now().date() + timedelta(days=7):
                    return render(request, "attendance.html", {
                        "students": students,
                        "year": datetime.now().year,
                        "today_date": today_date,
                        "error": "Cannot mark attendance for dates too far in the future."
                    })
                    
            except ValueError:
                return render(request, "attendance.html", {
                    "students": students,
                    "year": datetime.now().year,
                    "today_date": today_date,
                    "error": "Invalid date format."
                })

            # Process attendance for each student
            attendance_marked = False
            for student in students:
                status = request.POST.get(f'attendance_{student.enroll}', '').strip()
                
                if status in ['Present', 'Absent', 'Leave']:
                    try:
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
                        attendance_marked = True
                        
                    except Exception as save_error:
                        logger.error(f"Error saving attendance for {student.enroll}: {str(save_error)}")
                        continue

            if attendance_marked:
                logger.info(f"Attendance marked by TG {tg_id} for date {attendance_date}")
                return redirect("/tghome/")
            else:
                return render(request, "attendance.html", {
                    "students": students,
                    "year": datetime.now().year,
                    "today_date": today_date,
                    "error": "No attendance was marked. Please select status for at least one student."
                })

        # GET request - show attendance form
        return render(request, "attendance.html", {
            "students": students,
            "year": datetime.now().year,
            "today_date": today_date,
        })
    
    except Exception as e:
        logger.error(f"Unexpected error in attendance function: {str(e)}")
        return render(request, "error.html", {
            "message": "Error processing attendance. Please try again."
        })

def view_attendance(request):
    """
    Teacher view attendance function - Production ready for Render deployment
    """
    try:
        # Session validation
        tgid = request.session.get("tid")
        department = request.session.get("tdepartment")
        
        if not tgid or not department:
            logger.warning("Unauthorized TG access attempt")
            return redirect("/logintg/")
        
        # Fetch students with error handling
        try:
            students = models.Register.objects.filter(
                branch=department, 
                role="student", 
                status=1
            ).order_by('name')
            
            if not students.exists():
                return render(request, "view_attendance.html", {
                    "attendance_data": [],
                    "from_date": "2025-06-01",
                    "to_date": date.today().strftime("%Y-%m-%d"),
                    "search": "",
                    "today_date": date.today(),
                    "message": "No active students found in your department."
                })
                
        except Exception as db_error:
            logger.error(f"Error fetching students for department {department}: {str(db_error)}")
            return render(request, "error.html", {
                "message": "Error loading student data. Please try again."
            })

        # Parse parameters safely
        today_date = date.today()
        from_date = request.GET.get("from_date", "").strip() or "2025-06-01"
        to_date = request.GET.get("to_date", "").strip() or today_date.strftime("%Y-%m-%d")
        search = request.GET.get("search", "").strip()

        # Validate dates
        try:
            from_dt = datetime.strptime(from_date, "%Y-%m-%d").date()
            to_dt = datetime.strptime(to_date, "%Y-%m-%d").date()
            
            if from_dt > to_dt:
                from_dt, to_dt = to_dt, from_dt
                from_date = from_dt.strftime("%Y-%m-%d")
                to_date = to_dt.strftime("%Y-%m-%d")
                
        except ValueError:
            logger.warning(f"Invalid date parameters from TG {tgid}: {from_date}, {to_date}")
            from_dt = datetime.strptime("2025-06-01", "%Y-%m-%d").date()
            to_dt = today_date
            from_date = from_dt.strftime("%Y-%m-%d")
            to_date = to_dt.strftime("%Y-%m-%d")

        attendance_data = []

        # Process each student
        for student in students:
            try:
                # Apply search filter
                if search:
                    if (search.lower() not in student.name.lower() and 
                        search not in student.enroll):
                        continue

                # Fetch attendance records
                records = models.Attendance.objects.filter(
                    enroll=student.enroll,
                    tg_id=tgid,
                    date__range=(from_dt, to_dt)
                )

                # Calculate statistics
                total_days = records.count()
                present = records.filter(status="Present").count()
                absent = records.filter(status="Absent").count()
                leave = records.filter(status="Leave").count()
                
                effective_days = max(total_days - leave, 0)
                percentage = (present / effective_days * 100) if effective_days > 0 else 0
                percentage = min(max(percentage, 0), 100)  # Clamp 0-100

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
                
            except Exception as student_error:
                logger.error(f"Error processing student {student.enroll}: {str(student_error)}")
                continue

        # Sort by name
        attendance_data.sort(key=lambda x: x['name'].lower())

        context = {
            "attendance_data": attendance_data,
            "from_date": from_date,
            "to_date": to_date,
            "search": search,
            "today_date": today_date,
        }

        return render(request, "view_attendance.html", context)
    
    except Exception as e:
        logger.error(f"Unexpected error in view_attendance: {str(e)}")
        return render(request, "error.html", {
            "message": "Error loading attendance data. Please try again."
        })


def student_view_attendance(request):
    """
    Student view attendance function - Production ready for Render deployment
    """
    try:
        # Session validation
        enroll = request.session.get("senroll")
        sname = request.session.get("sname")
        
        if not enroll:
            logger.warning("Student access attempt without enrollment session")
            return redirect('/login/')
        
        # Fetch student record with error handling
        try:
            student = models.Register.objects.get(enroll=enroll, role="student", status=1)
        except models.Register.DoesNotExist:
            logger.error(f"Student not found for enrollment: {enroll}")
            return render(request, "error.html", {
                "message": "Student record not found. Please contact administrator."
            })
        except Exception as db_error:
            logger.error(f"Database error fetching student {enroll}: {str(db_error)}")
            return render(request, "error.html", {
                "message": "Database connection error. Please try again later."
            })

        # Set safe default dates for production
        try:
            default_from_date = date(2025, 6, 1) 
            default_to_date = date.today()
        except Exception as date_error:
            logger.error(f"Date creation error: {str(date_error)}")
            default_from_date = date(2024, 1, 1)
            default_to_date = date(2025, 12, 31)

        # Parse query parameters safely
        from_date = request.GET.get("from_date", "").strip()
        to_date = request.GET.get("to_date", "").strip()
        
        if not from_date:
            from_date = default_from_date.strftime("%Y-%m-%d")
        if not to_date:
            to_date = default_to_date.strftime("%Y-%m-%d")

        # Validate and parse dates
        try:
            from_dt = datetime.strptime(from_date, "%Y-%m-%d").date()
            to_dt = datetime.strptime(to_date, "%Y-%m-%d").date()
            
            # Validate date range
            if from_dt > to_dt:
                from_dt, to_dt = to_dt, from_dt
                
        except ValueError as ve:
            logger.warning(f"Invalid date format from user {enroll}: {from_date}, {to_date}")
            from_dt = default_from_date
            to_dt = default_to_date
            from_date = from_dt.strftime("%Y-%m-%d")
            to_date = to_dt.strftime("%Y-%m-%d")

        # Fetch attendance records with error handling
        try:
            attendance_records = models.Attendance.objects.filter(
                enroll=enroll,
                date__range=(from_dt, to_dt)
            ).order_by("date")
        except Exception as db_error:
            logger.error(f"Error fetching attendance for {enroll}: {str(db_error)}")
            return render(request, "error.html", {
                "message": "Error retrieving attendance data. Please try again."
            })

        # Calculate statistics safely
        try:
            total_days = attendance_records.count()
            present = attendance_records.filter(status="Present").count()
            absent = attendance_records.filter(status="Absent").count()
            leave = attendance_records.filter(status="Leave").count()

            effective_days = max(total_days - leave, 0)  # Prevent negative values
            percentage = (present / effective_days * 100) if effective_days > 0 else 0
            percentage = min(max(percentage, 0), 100)  # Clamp between 0-100
            
        except Exception as calc_error:
            logger.error(f"Error calculating attendance stats for {enroll}: {str(calc_error)}")
            total_days = present = absent = leave = 0
            percentage = 0

        # Prepare context safely
        context = {
            "student": student,
            "records": attendance_records,
            "from_date": from_date,
            "to_date": to_date,
            "total_days": total_days,
            "present": present,
            "absent": absent,
            "leave": leave,
            "percentage": round(percentage, 2),
            "sname": sname or "Student",
        }

        return render(request, "student_view_attendance.html", context)
        
    except Exception as e:
        logger.error(f"Unexpected error in student_view_attendance: {str(e)}")
        return render(request, "error.html", {
            "message": "An unexpected error occurred. Please try again or contact support."
        })

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
    try:
        email = request.session.get("semail")
        if not email:
            return redirect("/login/") 

        user = models.Register.objects.filter(email=email).first()
        if not user:
            return redirect("/login/")

        if request.method == "POST":
            # Validate required fields
            name = request.POST.get("name", "").strip()
            dob = request.POST.get("dob", "").strip()
            gender = request.POST.get("gender", "").strip()
            mobile = request.POST.get("mobile", "").strip()
            address = request.POST.get("address", "").strip()
            course = request.POST.get("course", "").strip()
            branch = request.POST.get("branch", "").strip()
            year = request.POST.get("year", "").strip()

            if not all([name, dob, gender, mobile, course, branch, year]):
                return render(request, "editprofile.html", {
                    "user": user,
                    "error": "All fields except address and password are required.",
                    "branches": ["CSE", "IT", "CSE-AI", "CSE-DS", "Mechanical", "Electrical", "Civil"],
                    "years": ["2022-2026", "2023-2027", "2024-2028", "2025-2029"],
                    "courses": ["B.Tech", "Diploma"]
                })

            # Check if mobile is being changed and is not already taken
            if mobile != user.mobile:
                existing_mobile = models.Register.objects.filter(mobile=mobile).exclude(email=email).first()
                if existing_mobile:
                    return render(request, "editprofile.html", {
                        "user": user,
                        "error": "Mobile number already registered by another user.",
                        "branches": ["CSE", "IT", "CSE-AI", "CSE-DS", "Mechanical", "Electrical", "Civil"],
                        "years": ["2022-2026", "2023-2027", "2024-2028", "2025-2029"],
                        "courses": ["B.Tech", "Diploma"]
                    })

            user.name = name
            user.dob = dob
            user.gender = gender
            user.mobile = mobile
            user.address = address
            user.course = course
            user.branch = branch
            user.year = year

            # Optional password change
            new_password = request.POST.get("password", "").strip()
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
    except Exception as e:
        print(f"Error in editprofile: {e}")
        return render(request, "error.html", {"message": "Error updating profile. Please try again."})

def logout_student(request):
    request.session.flush()
    return redirect("/")

def logout_tg(request):
    request.session.flush()
    return redirect("/")

