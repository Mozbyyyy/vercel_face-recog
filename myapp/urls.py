# from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .Initialization import OverallRecord
from .Initialization import EmployeeMain
from .views import employee_count
from .views import employee_late
from .views import employee_early
from .views import get_name
from django.contrib.auth import views as auth_views
# from .views import get_next_code
from django.views.generic.base import TemplateView
from .Initialization.EmployeeMain import EmployeeDetails
from .Initialization.BranchMain import BranchList
from .Initialization.BranchMain import BranchDetails
from .Initialization.RequestForm import RequestForms
from .Initialization.RequestForm import search_view




  



# from .views import employee_attendance_view
urlpatterns = [
     path('', views.login_view, name='login'),
     path('home/', OverallRecord.home, name='home'),
     path('logout/', views.CustomLogoutView.as_view(), name='logout'),
     path('addemployee/', views.addemployee, name="addemployee"),
     
   #   path('get_next_code/', get_next_code, name='get_next_code'),
     # path('facedetection/', TemplateView.as_view(template_name='temp_myapp/facedetection.html'), name="facedetection"),
     path('EmployeeDetails/<str:user_id>/', EmployeeMain.EmployeeDetails, name="EmployeeDetails"),
     path('facedetection/',views.facedetection, name='facedetection'),
     path('camera_feed/', views.camera_feed, name='camera_feed'),
     path('get_name/', get_name, name='get_name'),
     path('get_attendance_data/', views.get_attendance_data, name='get_attendance_data'),
     path('employee_count/', employee_count, name='employee_count'),
     path('employee_late/', employee_late, name='employee_late'),
     path('employee_early/', employee_early, name='employee_early'),
     path('EmployeeDetails/', EmployeeDetails, name='EmployeeDetails'),
     path('BranchList/', BranchList, name='BranchList'),
     path('BranchDetails/', BranchDetails, name='BranchDetails'),
     path('BranchDetails/<str:branch>', BranchDetails, name='BranchDetails'),
     path('RequestForms/', RequestForms, name='RequestForms'),
     path('search_view/', search_view, name='search_view'),
     path('filter_and_fetch/', OverallRecord.filter_and_fetch, name='filter_and_fetch'),
     path('update_selected_key/',views.update_selected_key,name='update_selected_key'),
     path('employee/<str:emp_id>/', OverallRecord.view_employee_info, name='view_employee_info'),
     path('home/print-page/', OverallRecord.PrintPage, name='PrintPage'),
     path('get_daily_records/', OverallRecord.get_daily_records, name='get_daily_records'),
     path('get_attendance_employee/', OverallRecord.get_attendance_employee, name='get_attendance_employee')

     
     
     # path('latest_employee/', latest_employee, name='latest_employee'),
  ]

