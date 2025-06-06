from django.shortcuts import redirect

class SimpleAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        print("Middleware triggered for:", path)  # Debugging

        # Protect student routes
        protected_student_paths = [
            '/studenthome', '/student_view_attendance', '/viewreports', '/viewTT', '/viewnotes' , '/uploadassign' , '/student_notifications' , '/editprofile',
        ]
        if any(path.startswith(p) for p in protected_student_paths):
            if not request.session.get('sname'):
                print("Redirecting student to login.")
                return redirect('/login/')

        # Protect TG routes
        protected_tg_paths = [
            '/tghome', '/managestudent', '/attendance', '/view_attendance', '/editTT', '/addnotes', '/addreports', '/verifyassign' , '/notify', 
        ]
        if any(path.startswith(p) for p in protected_tg_paths):
            if not request.session.get('tname'):
                print("Redirecting TG to logintg.")
                return redirect('/logintg/')

        return self.get_response(request)
