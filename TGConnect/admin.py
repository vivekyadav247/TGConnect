from django.contrib import admin
from .models import RegisterTG, Register, Attendance, UploadAssignment, addreports

# Models ko admin panel mein register karo
admin.site.register(RegisterTG)
admin.site.register(Register)
admin.site.register(Attendance)
admin.site.register(UploadAssignment)
admin.site.register(addreports)
