
from django.shortcuts import render, get_object_or_404
from ..models import Branches, Employee
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def BranchList(request):
      return render(request, 'temp_myapp/BranchList.html')

def BranchList(request):
      branches = Branches.objects.all()
      return render(request, 'temp_myapp/BranchList.html', {'branches':branches})

def BranchDetails(request, branch):
    branch_instance = get_object_or_404(Branches, BranchCode=branch)
    employee_list = Employee.objects.filter(BranchCode_id=branch)

    query = request.POST.get("searchquery", "")
    if query:
        employee_list = employee_list.filter(Q(EmpCode__icontains=query) | Q(Firstname__icontains=query))

    employee_count = employee_list.count()

    page = request.GET.get('page', 1)
    paginator = Paginator(employee_list, 5)

    try:
        employee_page = paginator.page(page)
    except PageNotAnInteger:
        employee_page = paginator.page(1)
    except EmptyPage:
        employee_page = paginator.page(paginator.num_pages)

    # Render the template
    return render(request, 'temp_myapp/BranchDetails.html', {'branch': branch_instance, 'employee_list': employee_page, 'query': query, 'employee_count': employee_count})