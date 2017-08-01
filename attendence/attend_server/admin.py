from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Attendance)
admin.site.register(Attend_Recodes)
admin.site.register(Images)
admin.site.register(Modules)
admin.site.register(User_Module_Permission)
admin.site.register(Student)
admin.site.register(Tutor_Students)
