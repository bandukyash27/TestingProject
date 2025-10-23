from django.contrib import admin

# Register your models here.
from app.models import *

admin.site.register(Employee)
admin.site.register(Attendance)


admin.site.register(UserProfile)
admin.site.register(Task)