from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.db import models
from datetime import date,datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save




#New Models
class Branches(models.Model):
    BranchCode = models.CharField(max_length=20,unique=True,primary_key=True)
    Company = models.CharField(max_length=50)
    Location = models.CharField(max_length=50)
    Employees = models.CharField(max_length=10)
    BranchImage = models.ImageField(upload_to='branch_image/', null=True, blank=True)

class Employee(models.Model):
    EmpCode = models.CharField(max_length=20,unique=True,primary_key=True)
    BranchCode = models.ForeignKey(Branches, on_delete = models.CASCADE, to_field = 'BranchCode', null = True)
    Firstname = models.CharField(max_length=20)
    Middlename = models.CharField(max_length=20)
    Lastname = models.CharField(max_length=20)
    DateofBirth = models.DateField(default=date(2000, 1, 1))
    BloodType = models.CharField(max_length=3, default="N/D")
    Gender = models.CharField(max_length=8, default="Male")
    CivilStatus = models.CharField(max_length=10, default="N/A")
    Address = models.CharField(max_length=50, default="N/D")
    Position = models.CharField(max_length=50)
    Department = models.CharField(max_length=50, default="N/A", null=True, blank=True)
    EmployementDate = models.DateField(default=date(2000, 1, 1))
    EmploymentStatus = models.CharField(max_length=15,default="Regular")
    EmpImage = models.ImageField(upload_to='emp_image/', null=True, blank=True)
   

class RequestForm(models.Model):
    FormID = models.AutoField(primary_key=True)
    EmpCode = models.ForeignKey(Employee, on_delete = models.CASCADE, to_field = 'EmpCode', null = True)
    SelectRequest = models.CharField(max_length = 30)
    BeginTimeOff = models.DateTimeField()
    ConcludeTimeOff = models.DateTimeField()
    Range = models.CharField(max_length = 10,default='N/A')
    isApproved = models.BooleanField(default=False)
    Remarks = models.CharField(max_length = 100)
    created_at = models.DateTimeField(default=timezone.now)  
    date = models.DateField(default=date(2000, 1, 1))

class AttendanceCount(models.Model):
    ID = models.AutoField(primary_key=True)
    EmpCode = models.ForeignKey(Employee, on_delete=models.CASCADE, to_field='EmpCode', null=True)
    Vacation = models.FloatField(default= 0)
    Sick = models.FloatField(default = 0)
    GracePeriod = models.IntegerField(default=15)
    last_grace_period_month  = models.DateTimeField(default=date(2024, 1, 1))
    last_leaves_year = models.DateField(default=date(2024, 1, 1))


class DailyRecord(models.Model):
    ID = models.AutoField(primary_key=True)
    EmpCode = models.ForeignKey(Employee, on_delete=models.CASCADE, to_field='EmpCode', null=True)
    Empname = models.CharField(max_length=50, default = 'Unknown')
    date = models.DateField(default=date.today)
    timein = models.TimeField(blank=True, null=True)
    timeout = models.TimeField(blank=True, null=True)
    breakout = models.TimeField(blank=True, null=True)
    breakin = models.TimeField(blank=True, null=True)
    totallateness = models.CharField(default='00:00', max_length=50)
    latecount = models.CharField(default = '0', max_length = 6)
    totalundertime = models.CharField(default='00:00',max_length= 8)
    totalovertime = models.CharField(default='00:00:00', max_length= 8)
    created_at = models.DateTimeField(default=timezone.now)  
    approveOT = models.BooleanField(default=False)
    late = models.CharField(default = "None", max_length = 10)
    absent = models.CharField(default = "None", max_length = 10)
    remarks =models.CharField(default = "None", max_length = 30)
    class Meta:
        db_table = 'attendance'
        get_latest_by = 'date'



class temporray(models.Model):
    employee_number = models.CharField(max_length=100)
    Empname = models.CharField(max_length=50, default = 'Unknown')
    date = models.DateField(default=date.today)
    timein_names = models.CharField(max_length=100,null=True,blank=True)
    timeout_names = models.CharField(max_length=100,null=True,blank=True)
    breakout_names = models.CharField(max_length=100,null=True,blank=True)
    breakin_names = models.CharField(max_length=100,null=True,blank=True)
    timein_timestamps = models.DateTimeField(null=True,blank=True)
    breakout_timestamps = models.DateTimeField(null=True,blank=True)
    breakin_timestamps = models.DateTimeField(null=True,blank=True)
    timeout_timestamps = models.DateTimeField(null=True,blank=True)
    afternoonBreakin_timestamps = models.DateTimeField(null=True,blank=True)
    afternoonTimeout_timestramps = models.DateTimeField(null=True,blank=True)

    class Meta:
        db_table = 'temporay'

class EmployeeStatus(models.Model):
    ID = models.AutoField(primary_key=True)
    # DailyRecord = models.ForeignKey(DailyRecord, on_delete=models.CASCADE, to_field= 'ID', null=True)
    RequestForm = models.ForeignKey(RequestForm, on_delete=models.CASCADE, to_field= 'FormID', null=True) 
    RequestDate = models.DateField(default=date(2000, 1, 1))
    totallateness = models.FloatField(default = 00)
    totalabsent = models.FloatField(default = 00)
    totalundertime = models.FloatField(default = 00)
    totalovertime = models.FloatField(default = 00)


        
            
# @receiver(pre_save, sender=Student)
# def generate_code(sender, instance, **kwargs):
#     if not instance.code:
#         # Increment the number and format the new code
#         current_number = Student.objects.count() + 10000
#         new_code = f"EMB{current_number:05d}"
#         instance.code = new_code