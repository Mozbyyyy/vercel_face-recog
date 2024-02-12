
from datetime import datetime, time, timedelta
from ..models import Employee, AttendanceCount
from ..models import DailyRecord
from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import urlencode
import math


def EmployeeDetails(request):
      return render(request, 'temp_myapp/EmployeeDetails.html')

# This is the calculation for overtime
def CalculateOvertime(attendance_records):
    total_overtime_sum = 0 

    for record in attendance_records:
        
        if record.timeout and record.approveOT:
            timeout_datetime = datetime.combine(record.date, record.timeout)

            upper_bound = datetime.combine(record.date, time(16, 0, 0))

            if timeout_datetime > upper_bound:
                time_difference = timeout_datetime - upper_bound

                if time_difference.total_seconds() >= 3600:
                    total_overtime_sum += time_difference.total_seconds()

                    record.totalovertime = time_difference
                    record.save()

    total_hours, total_remainder = divmod(total_overtime_sum, 3600)
    total_minutes, _ = divmod(total_remainder, 60)
       
    total_overtime_str = f"{int(total_hours):02d}:{int(total_minutes):02d}"

    return total_overtime_str




# This is the calculation for undertime
def calculate_undertime_for_record(record, field_name, upper_bound_time):
    undertime_duration = timedelta()

    field_value = getattr(record, field_name)

    if field_value:
        field_datetime = datetime.combine(record.date, field_value)

        if field_datetime < datetime.combine(record.date, upper_bound_time):
            undertime_duration = max(datetime.combine(record.date, upper_bound_time) - field_datetime, timedelta())

    return undertime_duration

def count_undertime_intervals(undertime_duration):
    interval_duration = timedelta(minutes=15)
    undertime_count = math.ceil(undertime_duration.total_seconds() / interval_duration.total_seconds())

    return undertime_count



def CalculateUndertime(attendance_records):
    total_undertime = timedelta()
    total_undertime_count = 0

    for record in attendance_records:
        if record.timeout != time(0, 0):  # Check if timeout is not midnight
            # Convert record.timeout to string and then to timedelta for comparison
            
            undertime_duration = calculate_undertime_for_record(record, "timeout", time(16, 0, 0))

            # Check if undertime_duration is not equal to zero timedelta
            if undertime_duration != timedelta():
                total_undertime += undertime_duration
                record.totalundertime = undertime_duration
                record.save()
                undertime_count = count_undertime_intervals(undertime_duration)
                total_undertime_count += undertime_count

    return total_undertime


# This is the calculation for lateness
def CalculateLateness(attendance_records):
    total_lateness_count = 0

    for record in attendance_records:
        total_lateness_count += int(record.latecount)

    return total_lateness_count


# This is the calculation for Gracce Period
def Grace_Period(user, current_time_str):
    if current_time_str:
        current_time = datetime.strptime(current_time_str, "%H:%M:%S")
        fixed_time = datetime.combine(current_time.date(), time(7, 0, 0))

        total_lateness = max(current_time - fixed_time, timedelta())

        attendance_count = AttendanceCount.objects.get(EmpCode=user)
        current_grace_period = timedelta(minutes=attendance_count.GracePeriod)

        new_grace_period = max(current_grace_period - total_lateness, timedelta(minutes=0))

        attendance_count.GracePeriod = new_grace_period.total_seconds() // 60
        attendance_count.save()



        

def EmployeeDetails(request, user_id):
    user = get_object_or_404(Employee, EmpCode=user_id)

    current_month = request.current_time.month

    attendance_records = DailyRecord.objects.filter(EmpCode_id=user, date__month = current_month).order_by('-created_at')
    
    attendance_count = AttendanceCount.objects.get(EmpCode=user)
    branch_name = user.BranchCode.Company if user.BranchCode else None
    query = request.POST.get("searchquery", "")


    total_lateness_str = CalculateLateness(attendance_records)
    total_undertime_str = CalculateUndertime(attendance_records)
    total_overtime_str = CalculateOvertime(attendance_records)


    if query:
        attendance_records = attendance_records.filter(Q(date__icontains=query) | Q(created_at__icontains=query))

    page = request.GET.get('page', 1)
    paginator = Paginator(attendance_records, 5) 

    try:
        attendance_records = paginator.page(page)
    except PageNotAnInteger:
        attendance_records = paginator.page(1)
    except EmptyPage:
        attendance_records = paginator.page(paginator.num_pages)

    if request.method == "POST":
        if "add" in request.POST:
            EmpCode_id = request.POST.get("EmpCode_id")
            date =   request.POST.get("date")
            timein = request.POST.get("timein")
            timeout = request.POST.get("timeout")
            breakout = request.POST.get("breakout")
            breakin = request.POST.get("breakin")
            approveOT = bool(request.POST.get("approveOT"))
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            employee_name = get_object_or_404(Employee, EmpCode=EmpCode_id)
           
            Grace_Period(EmpCode_id,timein)
           
            DailyRecord.objects.create(
                EmpCode_id=EmpCode_id,
                date=date,
                timein=timein,
                timeout=timeout,
                breakout=breakout,
                breakin=breakin,
                approveOT= approveOT,
                created_at=created_at,
                Empname = f"{employee_name.Firstname} {employee_name.Lastname}"
            )

          

            messages.success(request, 'Data added successfully!',extra_tags='added')   
            return HttpResponseRedirect(request.path)

      
        elif "update" in request.POST:
            EmpCode_id = request.POST.get("EmpCode_id")
            date_str = request.POST.get("date")
            timein = request.POST.get("timein")
            timeout = request.POST.get("timeout")
            breakout = request.POST.get("breakout")
            breakin = request.POST.get("breakin")
            approveOT = bool(request.POST.get("approveOT"))
            created_at = request.POST.get("created_at")
            date = datetime.strptime(date_str, "%b. %d, %Y").strftime("%Y-%m-%d")

            update_dtr = DailyRecord.objects.get(EmpCode_id=EmpCode_id, date=date)
            update_dtr.date = date
            update_dtr.timein = timein
            update_dtr.timeout = timeout
            update_dtr.breakout = breakout
            update_dtr.breakin = breakin
            update_dtr.created_at = created_at
            update_dtr.approveOT= approveOT
            update_dtr.save()

          

            messages.success(request, 'Data updated successfully!', extra_tags='updated')
            return HttpResponseRedirect(request.path)
        
        elif "delete" in request.POST:
            EmpCode_id = request.POST.get("deleteEmpCode")
            date_str = request.POST.get("deleteDate")
            date = datetime.strptime(date_str, "%b. %d, %Y").strftime("%Y-%m-%d")

            DailyRecord.objects.get(EmpCode_id=EmpCode_id, date=date).delete()

            messages.success(request, 'Record deleted successfully!', extra_tags='deleted')

            return HttpResponseRedirect(request.path)
        

        
        
    elif "search" in request.POST: 
            query = request.POST.get("searchquery", "")
            if query:
                attendance_records = attendance_records.filter(Q(date__icontains=query) | Q(created_at__icontains=query))
            else:
                attendance_records = DailyRecord.objects.all().order_by('created_at')
            
            paginator = Paginator(attendance_records, 5)  # Reset paginator
            page = request.GET.get('page', 1)

            try:
                attendance_records = paginator.page(page)
            except PageNotAnInteger:
                attendance_records = paginator.page(1)
            except EmptyPage:
                attendance_records = paginator.page(paginator.num_pages)

            return render(request, 'temp_myapp/EmployeeDetails.html', {'user_id': user_id,'branch_name': branch_name,'attendance_count': attendance_count,'user': user,'attendance_records': attendance_records, 'query': query})

    context = {
        'user_id': user_id,
        'branch_name': branch_name,
        'attendance_count': attendance_count, 
        'user': user,
        'attendance_records': attendance_records,
        'query': query,
        'total_lateness_sum': total_lateness_str,
        'total_undertime_sum': total_undertime_str,
        'total_overtime_sum':total_overtime_str
    }

    return render(request, 'temp_myapp/EmployeeDetails.html',context)

