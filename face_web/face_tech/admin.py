from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Group)
admin.site.register(Person)
admin.site.register(Person_To_Group)
admin.site.register(Face)
