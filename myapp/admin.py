from django.contrib import admin
from . import models


# Register your models here.

admin.site.register(models.Branches)
admin.site.register(models.Employee)
admin.site.register(models.EmployeeStatus)
admin.site.register(models.RequestForm)
admin.site.register(models.AttendanceCount)
admin.site.register(models.DailyRecord)
admin.site.register(models.temporray)
