
from django.shortcuts import render, get_object_or_404
from ..models import Branches, Employee, RequestForm, AttendanceCount
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse


def create_request(request_type, DeductRange, EmpCode_id, is_approved, remarks, attendace_count, requestdate):
    default_date = "2023-12-20"
    static_begin_time_off = datetime.strptime(f"{default_date}T07:00:00", "%Y-%m-%dT%H:%M:%S")
    static_conclude_time_off = datetime.strptime(f"{default_date}T16:00:00", "%Y-%m-%dT%H:%M:%S")

    dynamic_date = datetime.strptime(requestdate, "%Y-%m-%d").strftime("%Y-%m-%d")
    static_begin_time_off = static_begin_time_off.replace(year=int(dynamic_date[:4]), month=int(dynamic_date[5:7]), day=int(dynamic_date[8:10]))
    static_conclude_time_off = static_conclude_time_off.replace(year=int(dynamic_date[:4]), month=int(dynamic_date[5:7]), day=int(dynamic_date[8:10]))

    if DeductRange == "AM":
        static_conclude_time_off = datetime.strptime(f"{dynamic_date}T12:00:00", "%Y-%m-%dT%H:%M:%S")
    elif DeductRange == "PM":
        static_begin_time_off = datetime.strptime(f"{dynamic_date}T13:00:00", "%Y-%m-%dT%H:%M:%S")

    RequestForm.objects.create(
        EmpCode_id=EmpCode_id,
        SelectRequest=request_type,
        BeginTimeOff=static_begin_time_off,
        Range=DeductRange,
        ConcludeTimeOff=static_conclude_time_off,
        isApproved=is_approved,
        Remarks=remarks,
    )

    deduction_value = 0.5 if DeductRange in ["AM", "PM"] else 1.0

    if request_type == "Vacation":
        attendace_count.Vacation -= deduction_value
    elif request_type == "Sick":
        attendace_count.Sick -= deduction_value

def RequestForms(request):
        query = request.POST.get("searchquery", "")

        if query:
                form_list = RequestForm.objects.filter(  Q(BeginTimeOff__icontains=query) | Q(ConcludeTimeOff__icontains=query) | Q(EmpCode__Lastname__icontains=query))
        else:
                form_list = RequestForm.objects.all().order_by('created_at')
                
        page = request.GET.get('page', 1)
        paginator = Paginator(form_list, 7)  

        try:
                form_list = paginator.page(page)
        except PageNotAnInteger:
                form_list = paginator.page(1)
        except EmptyPage:
                form_list = paginator.page(paginator.num_pages)

        possible_deductrange = ['AM', 'PM', 'Whole']
        possible_request = ['Locator', 'Trip Ticket', 'Sick', 'Vacation', 'Paternity']
        context = {
                'possible_request':possible_request,
                'possible_deductrange':possible_deductrange,
                'form_list': form_list,

        }
            
        if request.method == "POST":
                if "add" in request.POST:
                        EmpCode_id = request.POST.get('Empcode')
                        request_type = request.POST.get('Request')
                        out_time_date = request.POST.get('OutTimeDate')
                        in_time_date = request.POST.get('InTimeDate')
                        is_approved = request.POST.get('isapproved') == "true"
                        DeductRange = request.POST.get('DeductRange')
                        remarks = request.POST.get('remarks')
                        requestdate = request.POST.get('requestdate')

                        attendace_count = AttendanceCount.objects.get(EmpCode_id=EmpCode_id)

                        if out_time_date and in_time_date:
                                begin_time_off = datetime.strptime(in_time_date, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")
                                conclude_time_off = datetime.strptime(out_time_date, "%Y-%m-%dT%H:%M").strftime("%Y-%m-%d %H:%M:%S")

                                RequestForm.objects.create(
                                EmpCode_id=EmpCode_id,
                                SelectRequest=request_type,
                                BeginTimeOff=begin_time_off,
                                Range = "N/A",
                                ConcludeTimeOff=conclude_time_off,
                                isApproved=is_approved,
                                Remarks=remarks,
                                        )
                                
                                messages.success(request, 'Request Submmited Successfully.', extra_tags='added')

                        elif not(out_time_date and in_time_date) and request_type in ["Vacation", "Sick", "Paternity"] and (attendace_count.Vacation > 0 or attendace_count.Sick > 0):
                                try:
                                    create_request(request_type, DeductRange, EmpCode_id, is_approved, remarks,attendace_count,requestdate) 
                                    attendace_count.save()
                                
                                    messages.success(request, 'Request Submmited Successfully.', extra_tags='added')

                                except AttendanceCount.DoesNotExist:
                                        print("AttendanceCount not found for the specified EmpCode")
                        else:
                                messages.success(request, "Employee has not been granted any leaves yet.", extra_tags='NoLeave')

                        return HttpResponseRedirect(request.path)
                
                elif "delete" in request.POST:
                        FormID = request.POST.get("FormID")
                        EmpCode_id = request.POST.get('EmpCode')
                        Range = request.POST.get('Range')
                        RequestType = request.POST.get('RequestType')
                        RequestForm.objects.get(FormID=FormID).delete()
                        attendace_count = AttendanceCount.objects.get(EmpCode_id=EmpCode_id)

                        deduction_value = 0.5 if Range in ["AM", "PM"] else 1.0

                        if RequestType == "Vacation":
                            attendace_count.Vacation += deduction_value
                        elif RequestType == "Sick":
                            attendace_count.Sick += deduction_value
                        attendace_count.save()
                        messages.success(request, 'Data deleted successfully!',extra_tags='delete')
                        return redirect('RequestForms')
                
   
        

        elif "search" in request.POST: 
            query = request.POST.get("searchquery", "")
            if query:
                attendance_records = attendance_records.filter(Q(isApproved__icontains=query) | Q(created_at__icontains=query))
            else:
                attendance_records = RequestForm.objects.all().order_by('created_at')
            
            paginator = Paginator(attendance_records, 5)  # Reset paginator
            page = request.GET.get('page', 1)

            try:
                attendance_records = paginator.page(page)
            except PageNotAnInteger:
                attendance_records = paginator.page(1)
            except EmptyPage:
                attendance_records = paginator.page(paginator.num_pages)
            
    
            return render(request, 'temp_myapp/EmployeeDetails.html', {'attendance_records': attendance_records, 'query': query,}, context)   
        
      
     
        return render(request, 'temp_myapp/RequestForm.html', context)



def search_view(request):
    try:
        query = request.GET.get('query', '')
        results = Employee.objects.filter(EmpCode__icontains=query)
        data = [{'EmpCode': obj.EmpCode, 'empcode': obj.EmpCode} for obj in results]
        return JsonResponse({'data': data})
    except Exception as e:
        print(f'Error in search_view: {str(e)}')
        return JsonResponse({'error': str(e)}, status=500)
