from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .models import Employee, Branches,DailyRecord,AttendanceCount, temporray
import logging
from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt 
from django.db.models import Q, F, When, Case, Value, TimeField
from django.contrib import messages
from django.http import HttpResponseRedirect
# from .UserTesting import main
import base64
import cv2
from django.http import StreamingHttpResponse

import face_recognition
import os
import dlib
import math
import numpy as np
from functools import lru_cache
import time
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor

from datetime import datetime, time, date
from django.db import transaction
from django.http import JsonResponse
from django.http import HttpResponse


from django.utils import timezone
from datetime import timedelta

from scripts.multiprocessing_script import load_known_faces

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


def is_admin(user):
    return user.groups.filter(name='admingroup').exists()

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def addemployee(request):
    emp_code = request.GET.get('empCode')
    print(f"Received employee ID (empCode parameter): {emp_code}")
    query = request.POST.get("searchquery", "")
    if query:
        employee_list = Employee.objects.filter(Q(Firstname__icontains=query) | Q(Lastname__icontains=query) | Q(EmpCode__icontains=query))
    else:
        employee_list = Employee.objects.all().order_by('EmpCode')
        
    page = request.GET.get('page', 1)
    paginator = Paginator(employee_list, 7)  

    try:
        employee_list = paginator.page(page)
    except PageNotAnInteger:
        employee_list = paginator.page(1)
    except EmptyPage:
        employee_list = paginator.page(paginator.num_pages)
    
    branches = Branches.objects.all()
   
    if request.method == "POST":
        if "add" in request.POST:
            
            EmpCode = request.POST.get("EmpCode")
            Firstname = request.POST.get("Firstname")
            Middlename = request.POST.get("Middlename")
            Lastname = request.POST.get("Lastname")
            DateofBirth = request.POST.get("DateofBirth")
            BloodType = request.POST.get("BloodType")
            Gender = request.POST.get("Gender")
            CivilStatus = request.POST.get("CivilStatus")
            Address = request.POST.get("Address")
            Position = request.POST.get("Position")
            EmployementDate = request.POST.get("EmployementDate")
            EmploymentStatus = request.POST.get("EmploymentStatus")
            Department = request.POST.get("Department")
            BranchCode_id = request.POST.get("BranchCode_id")
            with transaction.atomic():
                employee = Employee.objects.create(
                    EmpCode=EmpCode,
                    Firstname=Firstname,
                    Middlename=Middlename,
                    Lastname=Lastname,
                    DateofBirth=DateofBirth,
                    BloodType=BloodType,
                    Gender=Gender,
                    CivilStatus=CivilStatus,
                    Address=Address,
                    Position=Position,
                    EmployementDate=EmployementDate,
                    EmploymentStatus=EmploymentStatus,
                    Department=Department,
                    BranchCode_id=BranchCode_id
                )
                 
                  
                internet_time = request.current_time

                employment_date = datetime.strptime(EmployementDate, '%Y-%m-%d').date()
                employment_years = (internet_time.date() - employment_date).days // 365

                leave_mapping = {1: 5, 2: 10, 3: 15}
                vacation_days = leave_mapping.get(employment_years, 0)
                sick_leave_days = leave_mapping.get(employment_years, 0)
                

                attendance_count, created = AttendanceCount.objects.get_or_create(EmpCode=employee)
                attendance_count.Vacation = vacation_days
                attendance_count.Sick = sick_leave_days
                attendance_count.GracePeriod = 15
                attendance_count.save()
       

            messages.success(request, 'Data added successfully!',extra_tags='added')   
            return HttpResponseRedirect(request.path)
            # return redirect('addemployee')
      
        elif "update" in request.POST:
            EmpCode = request.POST.get("EmpCode")
            Firstname = request.POST.get("Firstname")
            Middlename = request.POST.get("Middlename")
            Lastname = request.POST.get("Lastname")
            DateofBirth = request.POST.get("DateofBirth")
            BloodType = request.POST.get("BloodType")
            Gender = request.POST.get("Gender")
            CivilStatus = request.POST.get("CivilStatus")
            Address = request.POST.get("Address")
            Position = request.POST.get("Position")
            EmployementDate = request.POST.get("EmployementDate")
            EmploymentStatus = request.POST.get("EmploymentStatus")
            Department = request.POST.get("Department")
            BranchCode_id = request.POST.get("BranchCode_id")
            vacation = request.POST.get("vacation")
            sick = request.POST.get("sick")


            update_employee = Employee.objects.get(EmpCode=EmpCode)
            update_employee.Firstname = Firstname
            update_employee.Middlename = Middlename
            update_employee.Lastname = Lastname
            update_employee.DateofBirth = DateofBirth
            update_employee.BloodType = BloodType
            update_employee.Gender = Gender
            update_employee.CivilStatus = CivilStatus
            update_employee.Address = Address
            update_employee.Position = Position
            update_employee.EmployementDate = EmployementDate
            update_employee.EmploymentStatus = EmploymentStatus
            update_employee.Department = Department
            update_employee.BranchCode_id = BranchCode_id
            
            update_leaves = AttendanceCount.objects.get(EmpCode_id = EmpCode)
            if vacation:
                update_leaves.Vacation = vacation
            if sick:
                update_leaves.Sick = sick


            update_leaves.save()
            update_employee.save()
        
            messages.success(request, 'Data updated successfully!',extra_tags='updated')
            return HttpResponseRedirect(request.path)
        
        elif "delete" in request.POST:
            EmpCode = request.POST.get("EmpCode")
            print(f"Update: EmpCode = {EmpCode}")
            Employee.objects.get(EmpCode=EmpCode).delete()
            # Redirect after the form is successfully submitted
            return redirect('addemployee')
        
    elif "search" in request.POST: 
            query = request.POST.get("searchquery", "")
            if query:
                employee_list = Employee.objects.filter(Q(Firstname__icontains=query) | Q(Lastname__icontains=query) | Q(EmpCode__icontains=query))
            else:
                employee_list = Employee.objects.all().order_by('EmpCode')
            
            paginator = Paginator(employee_list, 7)  
            page = request.GET.get('page', 1)

            try:
                employee_list = paginator.page(page)
            except PageNotAnInteger:
                employee_list = paginator.page(1)
            except EmptyPage:
                employee_list = paginator.page(paginator.num_pages)

            return render(request, 'temp_myapp/addemployee.html', {'employee_list': employee_list, 'query': query})
    
    possible_statuses = ['Trainee', 'Probationary', 'Regular']
    possible_civil_status = ['Married', 'Single', 'Divorced']
    possible_gender = ['Male', 'Female']
    possible_department = ['Audit', 'Credit&Coll', 'Csp', 'Financial', 'GRCD', 'Hr&Admin', 'M2', 'Management Accounting', 'MIS', 'Operation','PSPMI', 'Transportation Lisence' ]
    
    context = {
        'employee_list': employee_list,
        'query': query,
        'branches': branches,
        'possible_statuses': possible_statuses,
        'possible_civil_status': possible_civil_status,
        'possible_gender': possible_gender,
        'possible_department': possible_department,
    }
   
    if emp_code:
       
        employee = Employee.objects.get(EmpCode=emp_code)
        attendance_count = AttendanceCount.objects.get(EmpCode_id=employee)

        context['getVlSl'] = {
           
            'Vacation': attendance_count.Vacation,
            'Sick': attendance_count.Sick,
        }

    return render(request, 'temp_myapp/addemployee.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'temp_myapp/login.html', {'form': form})




# def get_next_code(request):
#     latest_code = Student.objects.order_by('-code').first()
#     if latest_code:
#         current_number = int(latest_code.code[3:]) + 1
#     else:
#         current_number = 1

#     new_code = f"EMB{current_number:04d}"
#     return JsonResponse({'code': new_code})


# FACE DETECTIONNNNNNNNNNNNNNNNNNNNNNNNN


SHAPE_PREDICTOR_PATH = "myapp/assets/pre-trained/shape_predictor_68_face_landmarks.dat"
FRAME_WIDTH = 720
FRAME_HEIGHT = 420
THRESHOLD = 0.353
GLOBALNAME = ''


global_variable_name = ''
recognize_face_cache = {}
cache_exp = 60
inserted_names = set()
face_counters = {}
error_messages = []
threshold = 3

# Initialization of Face Encoding




# Main Function for Caching and Face Recogntion
def recognize_face(request, face_encoding, known_face_encodings, known_face_names, location,current_time):
  
    # need to change in internet time
    #current_time = datetime.now()
 

    if tuple(face_encoding) in recognize_face_cache and current_time - recognize_face_cache[tuple(face_encoding)]["timestamp"] < cache_exp:
        return recognize_face_cache[tuple(face_encoding)]["name"]

    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=THRESHOLD)

    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]
         
        if name not in face_counters:
            face_counters[name] = 0

        
        face_counters[name] += 1

    
        if face_counters[name] >= threshold:
            
            recognize_face_cache[tuple(face_encoding)] = {"name": name, "timestamp": current_time}

           
            face_counters[name] = 0

            
            for other_face_name in face_counters:
                if other_face_name != name and face_counters[other_face_name] <= 3:
                    face_counters[other_face_name] = 0

            
            max_name = recognize_face_cache[tuple(face_encoding)]["name"]

            employee_login_dtr(request, max_name, face_encoding,current_time)
            space_index = max_name.find(" ")
            if space_index != -1:
                employee_number = name[:space_index]
                employee_name = name[space_index + 1:]
            else:
                employee_number = None
                employee_name = None

            return employee_name
   
    return "Analyzing Face..."

    

# Preprocessing of frame 
def preprocess(frame):
    face_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return face_gray

# Data Augmentation specifically for lighting
def apply_lighting_augmentation(image, alpha, beta):
    augmented_image = cv2.addWeighted(image, alpha, np.zeros(image.shape, image.dtype), 0, beta)
    augmented_image = np.clip(augmented_image, 0, 255)
    return augmented_image

# Euclidean distance calcutlation for facial alignment
def calculate_eye_distance(left_eye, right_eye):
    delta_x = right_eye[0] - left_eye[0]
    delta_y = right_eye[1] - left_eye[1]
    angle = math.degrees(math.atan2(delta_y, delta_x))
    return angle


known_faces_dict = load_known_faces()
def update_selected_key(request):
    selected_key = request.POST.get('selected_key', '')
    request.session['selected_key'] = selected_key
    request.session.save()

    # Include the updated session value in the response
    response_data = {
        'status': 'success',
        'selected_key': selected_key
    }

    return JsonResponse(response_data)

# Main function for initialization of camera and face recognition
def gen_frames(request,selected_key_value=None):
    
    if 'selected_key' in request.session:
        selected_key_value = request.session['selected_key']
    else:
        # If not present, set the default value
        selected_key_value = "Csrd"
        request.session['selected_key'] = selected_key_value
        request.session.save()


    if selected_key_value not in known_faces_dict:
        print(f"Error: Key '{selected_key_value}' not found in known_faces_dict.")
        return HttpResponse(status=500)  # Return an error response if key not found

    selected_faces_dict = known_faces_dict[selected_key_value]
    known_face_encodings = selected_faces_dict['encodings']
    known_face_names = selected_faces_dict['names']

    cap = cv2.VideoCapture(0) 
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)

    frame_skip = 1
    frame_count = 0

    while True:
        success, frame = cap.read()  
        if not success:
            break
        
        if not success or frame is None:
            continue

        frame_count+=1

        if frame_count % frame_skip != 0:
            continue 

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            try:
                
              
                min_width = 40
                min_height = 40

                if face.width() < min_width or face.height() < min_height:
                    continue
               
                

                landmarks = predictor(gray, face)
                left_eye = (landmarks.part(36).x, landmarks.part(36).y)
                right_eye = (landmarks.part(45).x, landmarks.part(45).y)

             
                angle = calculate_eye_distance(left_eye, right_eye)

                reference_distance = np.linalg.norm(np.array(left_eye) - np.array(right_eye))
                distance_between_eyes = np.sqrt((right_eye[0] - left_eye[0]) ** 2 + (right_eye[1] - left_eye[1]) ** 2)
                scale_factor = distance_between_eyes / reference_distance

                rotation_matrix = cv2.getRotationMatrix2D(left_eye, angle, scale_factor)

                aligned_face = cv2.warpAffine(frame, rotation_matrix, (frame.shape[1], frame.shape[0]))

                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                aligned_face = aligned_face[y:y + h, x:x + w]

                aligned_face_rgb = preprocess(aligned_face)

             
                augmented_face = apply_lighting_augmentation(aligned_face_rgb, alpha=1.2, beta=30)

                face_locations = face_recognition.face_locations(augmented_face)
                face_encodings = face_recognition.face_encodings(augmented_face, face_locations)
                
      
                  # need to change in internet time
                #current_time = request.current_time
                
                current_time = datetime.now()
                batch_size =   3
                face_batches = [face_encodings[i:i + batch_size] for i in range(0, len(face_encodings), batch_size)]
                location_batches = [face_locations[i:i + batch_size] for i in range(0, len(face_locations), batch_size)]


                with ThreadPoolExecutor() as executor:
                    for face_batch, location_batch in zip(face_batches, location_batches):
                        futures = [executor.submit(recognize_face, request, face_encoding, known_face_encodings, known_face_names, location,current_time)
                                for face_encoding, location in zip(face_batch, location_batch)]

                        for future, (top, right, bottom, left) in zip(futures, location_batch):
                            name = future.result()
                            cv2.rectangle(frame, (left + x, top + y), (right + x, bottom + y), (2, 195, 154), 2)

                            text_size, _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_DUPLEX, 0.5, 1)

                            rect_width = text_size[0] + 20 
                            text_position = (left + x - 5, bottom + y + 15)
                            rect_position = (left + x - 10, bottom + y)

                            cv2.rectangle(frame, rect_position, (rect_position[0] + rect_width, rect_position[1] + 23), (255, 0, 0),
                                        thickness=cv2.FILLED)
                            font = cv2.FONT_HERSHEY_DUPLEX
                            cv2.putText(frame, name, text_position, font, 0.5, (255, 255, 255), 1)

                    
                    
            except Exception as e:
             
                print(f"An error occurred: {str(e)}")

        ret, buffer = cv2.imencode('.jpg', frame) 
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# Camera initialization
def camera_feed(request):
    selected_key_value = request.session.get('selected_key', 'Fin')
    return StreamingHttpResponse(gen_frames(request,selected_key_value), content_type='multipart/x-mixed-replace; boundary=frame')


# function for inserting timein, breakout, breakin , timeout in the database
def employee_login_dtr(request, name, face_encoding,current_time):
        # need to change in internet time
        #current_time = datetime.now()
       
   

    # Extract employee number and name from the input 'name'
        space_index = name.find(" ")
        if space_index != -1:
            employee_number = name[:space_index]
            employee_name = name[space_index + 1:]
        else:
            employee_number = None
            employee_name = None

        # Check if the employee has been inserted today
        prac_time = current_time.strftime("%H:%M")
        global global_variable_name
        recognize_face_cache[tuple(face_encoding)] = {"employee_number": employee_number, "timestamp": current_time.timestamp()}


    # Extracting location information
        if "06:00" <= prac_time <= "16:00":
            deleteTable()
            # ResetGraceAndLeaves()
            
            
        if "03:00" <= prac_time <= "09:59": 
            existing_entry = DailyRecord.objects.filter(EmpCode_id=employee_number,date=current_time.date()).first()
            if existing_entry is None: 
                insertData(employee_number, current_time,employee_name)
                temporray.objects.filter(employee_number=employee_number,date=current_time.date()).create(employee_number=employee_number,Empname=employee_name,timein_names=employee_number,timein_timestamps=current_time)
                global_variable_name = " Successfully TimeIn \n"+employee_name
                get_name(request)
                print("Successfully TimeIn block executed")


        
        if "12:00" <= prac_time <= "13:00" and temporray.objects.filter(employee_number=employee_number, timein_names__isnull=False, breakout_names__isnull=True, date=current_time.date()).exists():
            existing_entry = temporray.objects.filter(employee_number=employee_number, date=current_time.date()).first()
            
            existing_entry_timein_timestamps = existing_entry.timein_timestamps.replace(tzinfo=timezone.utc)
            current_time = current_time.replace(tzinfo=timezone.utc)
            
            time_difference = current_time - existing_entry_timein_timestamps
            remaining_seconds = max(15 - time_difference.total_seconds(), 0)
            
            if current_time - existing_entry_timein_timestamps >= timedelta(seconds=15):
                breakout(employee_number, current_time)  
                temporray.objects.filter(employee_number=employee_number, date=current_time.date()).update(breakout_names=employee_number,breakout_timestamps=current_time)
                global_variable_name = "Successfully BreakOut \n"+employee_name
                get_name(request)
                print("Successfully breakout block executed")
                return "Successfully Breakout..."
            else:
                return f"please wait...{int(remaining_seconds)} seconds"
        
        
        if "12:00" <= prac_time <= "14:00" and temporray.objects.filter(employee_number=employee_number, timein_names__isnull=False, breakout_names__isnull=False,breakin_names__isnull=True, date=current_time.date()).exists():
            existing_entry2 = temporray.objects.filter(employee_number=employee_number, date=current_time.date()).first()
            
            existing_entry_breakout_timestamps = existing_entry2.breakout_timestamps.replace(tzinfo=timezone.utc)
            current_time = current_time.replace(tzinfo=timezone.utc)

            time_difference = current_time - existing_entry_breakout_timestamps
            remaining_seconds = max(15 - time_difference.total_seconds(), 0)
            
            if current_time - existing_entry_breakout_timestamps >= timedelta(seconds=8):
                breakin(employee_number, current_time)  
                temporray.objects.filter(employee_number=employee_number, date=current_time.date()).update(breakin_names=employee_number,breakin_timestamps=current_time)
                global_variable_name = "Successfully BreakIn \n"+ employee_name
                get_name(request)
                print("Successfully BreakIn block executed")
                return "Successfully Breakin..."
            else:
                return f"please wait...{int(remaining_seconds)} seconds"
            
        if "15:00" <= prac_time <= "23:59" and temporray.objects.filter(employee_number=employee_number, timein_names__isnull=False, breakout_names__isnull=False,breakin_names__isnull=False, timeout_names__isnull=True,date=current_time.date()).exists():
            existing_entry3 = temporray.objects.filter(employee_number=employee_number, date=current_time.date()).first()
            print("im Executed")
            existing_entry_breakin_timestamps = existing_entry3.breakin_timestamps.replace(tzinfo=timezone.utc)
            current_time = current_time.replace(tzinfo=timezone.utc)
            
            time_difference = current_time - existing_entry_breakin_timestamps
            remaining_seconds = max(30 - time_difference.total_seconds(), 0)
            # if temporray.objects.filter(employee_number=employee_number,  timeout_timestamps__isnull=False):
            #     global_variable_name = "You Already TIMEOUT!!! \n"  + employee_name
            #     get_name(request)
            if current_time - existing_entry_breakin_timestamps >= timedelta(seconds=30):
                timeout(employee_number, current_time)  
                temporray.objects.filter(employee_number=employee_number, date=current_time.date()).update(breakin_names=employee_number,timeout_timestamps=current_time)
                global_variable_name = "Successfully TimeOut \n "+ employee_name
                get_name(request)
                print("Successfully Timeout block executed")
                return "Successfully Timeout..."
            else:
                return f"please wait...{int(remaining_seconds)} seconds"
        


       
        if "15:00" <= prac_time <= "23:59" and temporray.objects.filter(Q(breakin_names__isnull=True) | Q(breakout_names__isnull=False), employee_number=employee_number,timein_names__isnull=False, date=current_time.date()).exists():
            nobreak_out_in(employee_number, current_time)
            temporray.objects.filter(employee_number=employee_number, date=current_time.date()).update(timein_names=employee_number,timeout_timestamps=current_time)
            global_variable_name ="NO BEAKOUT AND BREAKIN! \n" + employee_name
            print(global_variable_name) 
            print("Successfully NO BEAKOUT AND BREAKIN block executed")
            get_name(request)

        

        #if login afternoon
        if "10:00" <= prac_time <= "23:59":
                existing_entry = DailyRecord.objects.filter(EmpCode_id=employee_number,date=current_time.date()).first()
                if existing_entry is None: 
                    afternoonBreakIn(employee_number, current_time, employee_name)
                    temporray.objects.filter(employee_number=employee_number,date=current_time.date()).create(employee_number=employee_number,Empname=employee_name,breakin_names=employee_number,afternoonBreakin_timestamps=current_time)
                    global_variable_name ="Succesfully BreakIn! \n" + employee_name
                    get_name(request)

                if "15:00" <= prac_time <= "23:59" and temporray.objects.filter(employee_number=employee_number, breakin_names__isnull=False, timeout_names__isnull=True, date=current_time.date()).exists():
                    existing_entry = temporray.objects.filter(employee_number=employee_number, date=current_time.date()).first()
                    
                    existing_entry_breakin_timestamps = existing_entry.afternoonBreakin_timestamps.replace(tzinfo=timezone.utc)
                    current_time = current_time.replace(tzinfo=timezone.utc)
                    
                    time_difference = current_time - existing_entry_breakin_timestamps
                    remaining_seconds = max(15 - time_difference.total_seconds(), 0)
                    
                    if current_time - existing_entry_breakin_timestamps >= timedelta(seconds=15):
                        afternoonTimeout(employee_number, current_time)  
                        temporray.objects.filter(employee_number=employee_number, date=current_time.date()).update(timeout_names=employee_number,afternoonTimeout_timestramps=current_time)
                        global_variable_name ="Succesfully TimeOut! \n" + employee_name
                        get_name(request)
                        return "Successfully Timeout..."
                    elif temporray.objects.filter(employee_number=employee_number,  timeout_names__isnull=False):
                        global_variable_name = "You Already TIMEOUT!!! \n"  + employee_name
                        get_name(request)
                    else:
                        return f"please wait...{int(remaining_seconds)} seconds"

        # Set the global variable
     

def afternoonBreakIn(employee_number,current_time,employee_name):
    formatted_time = current_time.strftime("%H:%M:%S")
    total_lateness = timedelta()

    fixed_time = time(11, 0, 0)
    timein_datetime = current_time.time()

    if timein_datetime > fixed_time:
        time_difference = datetime.combine(current_time.date(), timein_datetime) - datetime.combine(current_time.date(), fixed_time)
        time_difference = max(time_difference, timedelta())
        total_lateness += time_difference

    hours, remainder = divmod(total_lateness.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    lateness_count = count_lateness_intervals(total_lateness)
    total_lateness_str = f"{hours:02d}:{minutes:02d}"
    total_lateness_count_str = lateness_count

    attendance_count, created = AttendanceCount.objects.get_or_create(EmpCode=employee_number)

    current_grace_period = timedelta(minutes=attendance_count.GracePeriod)

    if total_lateness.total_seconds() > current_grace_period.total_seconds():
        # If lateness is 2 hours or more, set formatted_time to "00:00:00"
        if total_lateness >= timedelta(hours=2):
            formatted_time = formatted_time
            total_lateness = timedelta()
            hours, remainder = divmod(total_lateness.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            lateness_count = count_lateness_intervals(total_lateness)
            total_lateness_str = f"{hours:02d}:{minutes:02d}"
            total_lateness_count_str = lateness_count

            # Mark as absent AM
            DailyRecord.objects.create(
                EmpCode_id=employee_number,
                Empname=employee_name,
                date=current_time.date(),
                timein="00:00:00",
                breakout="00:00:00",
                absent="Absent",
                breakin=formatted_time,  # Use formatted_time here
                timeout="00:00:00"
            )
            temporray.objects.create(
            employee_number=employee_number,
            Empname=employee_name,
            date=current_time.date(),
            breakin_names=employee_number,
            afternoonBreakin_timestamps=current_time,
            timeout_names=employee_number,
            afternoonTimeout_timestramps=current_time
            )

        else:
            new_grace_period = timedelta(minutes=0)
            lateness_count = count_lateness_intervals(total_lateness)
            total_lateness_count_str = lateness_count
    else:
        new_grace_period = current_grace_period - total_lateness

    attendance_count.GracePeriod = new_grace_period.total_seconds() // 60
    attendance_count.save()

    if new_grace_period.total_seconds() == 0 and total_lateness > timedelta(minutes=0) or total_lateness > timedelta(minutes=0):
        # If grace period is 0, mark as late AM
        late_count = count_lateness_intervals(total_lateness)
        DailyRecord.objects.create(
            EmpCode_id=employee_number,
            Empname=employee_name,
            date=current_time.date(),
            timein="00:00:00",
            breakout="00:00:00",
            late="Late PM",
            absent = "Absent AM",
            totallateness=total_lateness_str,
            latecount=total_lateness_count_str,
            breakin=formatted_time  # Use formatted_time here
            
        )
    else:
        # Deduct from grace period
        DailyRecord.objects.create(
            EmpCode_id=employee_number,
            Empname=employee_name,
            date=current_time.date(),
            totallateness=total_lateness_str,
            absent = "Absent AM",
            timein="00:00:00",
            breakout="00:00:00",
            breakin=formatted_time  # Use formatted_time here
        )

    



def afternoonTimeout(employee_number,current_time):
    formatted_time = current_time.strftime("%H:%M:%S")
    DailyRecord.objects.filter(EmpCode_id=employee_number,breakin__isnull=False,date=current_time.date()).update(timeout=formatted_time)

def breakout(employee_number, current_time):
    formatted_time = current_time.strftime("%H:%M:%S")
    total_undertime = timedelta()

    # Check if there is an existing breakout value
    existing_entry = DailyRecord.objects.filter(
        timein__isnull=False,
        breakout__isnull=False,  # Check if breakout is not null
        EmpCode_id=employee_number,
        date=current_time.date()
    ).first()

    if existing_entry is not None and existing_entry.breakout != "00:00:00":
        # If breakout has a value, skip the update
        return

    breakout_datetime = datetime.combine(current_time.date(), current_time.time())
    upper_bound_breakout = datetime.combine(current_time.date(), time(12, 0, 0))

    if breakout_datetime < upper_bound_breakout:
        time_difference_breakout = upper_bound_breakout - breakout_datetime
        time_difference_breakout = max(time_difference_breakout, timedelta())

        total_undertime += time_difference_breakout

    hours, remainder = divmod(total_undertime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    total_undertime_str = f"{hours:02d}:{minutes:02d}"

   
    DailyRecord.objects.filter(
        timein__isnull=False,
        breakout__isnull=True,  
        EmpCode_id=employee_number,
        date=current_time.date()
    ).update(breakout=formatted_time, totalundertime=total_undertime_str)


def count_lateness_intervals(lateness_duration):
    interval_duration = timedelta(minutes=15)
    lateness_count = math.ceil(lateness_duration.total_seconds() / interval_duration.total_seconds())
    return lateness_count


def insertData(employee_number, current_time, employee_name):
    formatted_time = current_time.strftime("%H:%M:%S")
    total_lateness = timedelta()

    fixed_time = time(7, 0, 0)
    timein_datetime = current_time.time()

    if timein_datetime > fixed_time:
        time_difference = datetime.combine(current_time.date(), timein_datetime) - datetime.combine(current_time.date(), fixed_time)
        time_difference = max(time_difference, timedelta())
        total_lateness += time_difference

    hours, remainder = divmod(total_lateness.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    lateness_count = count_lateness_intervals(total_lateness)
    total_lateness_str = f"{hours:02d}:{minutes:02d}"
    total_lateness_count_str = lateness_count

    attendance_count, created = AttendanceCount.objects.get_or_create(EmpCode=employee_number)

    current_grace_period = timedelta(minutes=attendance_count.GracePeriod)

    if total_lateness.total_seconds() > current_grace_period.total_seconds():
        # If lateness is 2 hours or more, set formatted_time to "00:00:00"
        if total_lateness >= timedelta(hours=2):
            formatted_time = formatted_time
            total_lateness = timedelta()
            hours, remainder = divmod(total_lateness.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            lateness_count = count_lateness_intervals(total_lateness)
            total_lateness_str = f"{hours:02d}:{minutes:02d}"
            total_lateness_count_str = lateness_count

            # Mark as absent AM
            DailyRecord.objects.create(
                EmpCode_id=employee_number,
                Empname=employee_name,
                date=current_time.date(),
                absent="Absent AM",
                timein=formatted_time,  # Use formatted_time here
                breakout="00:00:00"
            )
            temporray.objects.create(
            employee_number=employee_number,
            Empname=employee_name,
            date=current_time.date(),
            timein_names=employee_number,
            timein_timestamps=current_time,
            breakout_names=employee_number,
            breakout_timestamps=current_time
            )

        else:
            remaining_lateness = total_lateness - current_grace_period
            new_grace_period = timedelta(minutes=0)
            lateness_count = count_lateness_intervals(remaining_lateness)
            total_lateness_count_str = lateness_count
    else:
        new_grace_period = current_grace_period - total_lateness

    attendance_count.GracePeriod = new_grace_period.total_seconds() // 60
    attendance_count.save()

    if new_grace_period.total_seconds() == 0 and total_lateness > timedelta(minutes=0) or total_lateness > timedelta(minutes=0):
        # If grace period is 0, mark as late AM
        
        DailyRecord.objects.create(
            EmpCode_id=employee_number,
            Empname=employee_name,
            date=current_time.date(),
            late="Late AM",
            totallateness=total_lateness_str,
            latecount=total_lateness_count_str,
            timein=formatted_time  # Use formatted_time here
            
        )
        print("this late am trigger")
    else:
        # Deduct from grace period
        DailyRecord.objects.create(
            EmpCode_id=employee_number,
            Empname=employee_name,
            date=current_time.date(),
            totallateness=total_lateness_str,
            timein=formatted_time  # Use formatted_time here
        )
def add_time_strings(time_str1, time_str2):
    h1, m1 = map(int, time_str1.split(':'))
    h2, m2 = map(int, time_str2.split(':'))

    total_minutes = (h1 + h2) * 60 + (m1 + m2)
    hours, minutes = divmod(total_minutes, 60)

    return f"{hours:02d}:{minutes:02d}"

def breakin(employee_number, current_time):
    formatted_time = current_time.strftime("%H:%M:%S")
    total_lateness = timedelta()

    if current_time:
        fixed_time = time(13, 0, 0)
        breakin_datetime = datetime.combine(current_time.date(), current_time.time())

        if breakin_datetime > datetime.combine(current_time.date(), fixed_time):
            time_difference = breakin_datetime - datetime.combine(current_time.date(), fixed_time)
            time_difference = max(time_difference, timedelta())
            total_lateness += time_difference

            attendance_record = DailyRecord.objects.filter(
                timein__isnull=False, breakout__isnull=False, breakin__isnull=True, EmpCode_id=employee_number,
                date=current_time.date()
            ).first()

            if attendance_record:
                # Update the 'late' field only when it's "Absent AM"
                if attendance_record.late == "Late AM":
                    attendance_record.late = "Late AM-PM"
                else:
                    attendance_record.late = "Late PM"

                # Update the 'absent' field if total lateness is more than 3 hours
                if total_lateness > timedelta(hours=3):
                    if attendance_record.absent == "Absent AM":
                        attendance_record.absent = "Absent"
                    else:
                        attendance_record.absent = "Absent PM"

                attendance_record.save()

        hours, remainder = divmod(total_lateness.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        lateness_count = count_lateness_intervals(total_lateness)
        total_lateness_str = f"{hours:02d}:{minutes:02d}"
        total_lateness_count_str = lateness_count
        print(total_lateness_count_str)

        existing_record = DailyRecord.objects.filter(
            timein__isnull=False, breakout__isnull=False, breakin__isnull=True,
            EmpCode_id=employee_number, date=current_time.date()
        ).first()

        if existing_record:
            # Add the new values to the existing values
            total_lateness_count_str = int(total_lateness_count_str) + int(existing_record.latecount)

            total_lateness_str = add_time_strings(total_lateness_str, existing_record.totallateness)

        attendance_count = AttendanceCount.objects.get(EmpCode=employee_number)

        current_grace_period = timedelta(minutes=attendance_count.GracePeriod)

        if total_lateness > current_grace_period:
            new_grace_period = timedelta(minutes=0)
            # Update the count only if the new_grace_period is equal to 0
            if new_grace_period == timedelta(minutes=0):
                total_lateness_count_str = int(total_lateness_count_str) + 1
        else:
            new_grace_period = current_grace_period - total_lateness
            total_lateness_count_str = 0

        attendance_count.GracePeriod = new_grace_period.total_seconds() // 60

        attendance_count.save()
       
        # Update the record with the new values
        DailyRecord.objects.filter(
            timein__isnull=False, breakout__isnull=False, breakin__isnull=True,
            EmpCode_id=employee_number, date=current_time.date()
        ).update(
            breakin=formatted_time, totallateness=total_lateness_str, latecount=total_lateness_count_str
        )

      
def timeout(employee_number,current_time):
    formatted_time = current_time.strftime("%H:%M:%S")

    total_undertime = timedelta()

    if current_time:
        timeout_datetime = datetime.combine(current_time.date(),current_time.time())
        upper_bound_timeout = datetime.combine(current_time.date(), time(16, 0, 0))

        if timeout_datetime < upper_bound_timeout:
            time_difference_timeout = upper_bound_timeout - timeout_datetime
            time_difference_timeout = max(time_difference_timeout, timedelta())

            total_undertime += time_difference_timeout

        hours, remainder = divmod(total_undertime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        total_undertime_str = f"{hours:02d}:{minutes:02d}"    
        DailyRecord.objects.filter(timein__isnull=False,breakin__isnull=False,breakout__isnull=False,timeout__isnull=True, EmpCode_id=employee_number, date=current_time.date()).update(timeout=formatted_time,totalundertime=total_undertime_str)



def nobreak_out_in(employee_number, current_time):
    DailyRecord.objects.filter(
        EmpCode_id=employee_number,
        date=current_time.date()
    ).update(
        timein="00:00:00",
        breakout="00:00:00",
        breakin="00:00:00",
        timeout="00:00:00",
        absent = "Absent"
    )


def deleteTable():
        temporray.objects.exclude(date=date.today()).delete()


def ResetGraceAndLeaves():
    current_month = datetime.now().month
    current_year = datetime.now().year

    for attendance_count in AttendanceCount.objects.all():
 
        last_month = attendance_count.last_grace_period_month.month
        last_year = attendance_count.last_leaves_year.year

        if last_month != current_month:

            attendance_count.GracePeriod = 15

        if last_year != current_year:
            internet_time = datetime.now()
            if attendance_count.EmpCode.EmployementDate is not None:
                employment_date = attendance_count.EmpCode.EmployementDate
                employment_years = (internet_time.date() - employment_date).days // 365

                leave_mapping = {1: 5, 2: 10, 3: 15}
                vacation_days = leave_mapping.get(employment_years, 0)
                sick_leave_days = leave_mapping.get(employment_years, 0)

                attendance_count.Vacation = vacation_days
                attendance_count.Sick = sick_leave_days

                attendance_count.last_leaves_year = timezone.now()

      
        attendance_count.last_grace_period_month = timezone.now()
        attendance_count.save()




def get_name(request):
    processed_name = f"{global_variable_name}"
    response_data = {'processed_name': processed_name, 'global_variable_name': global_variable_name}
    print(f'Response Data: {response_data}')
    return JsonResponse(response_data)


# sorting the list of data
def facedetection(request):
    attendances = DailyRecord.objects.all().order_by('ID')
    return render(request, 'temp_myapp/facedetection.html',{'attendances':attendances})


# fetching list of employee attendace to be display in table
def get_attendance_data(request):
    current_date = date.today()
    attendances = DailyRecord.objects.filter(date=current_date).order_by('-created_at')
    
    def custom_sort(attendance):
        times = [attendance.breakout, attendance.breakin, attendance.timeout]
        latest_time = max(filter(None, times), default=None)  

        if latest_time is not None:
            latest_time = datetime.strptime(str(latest_time), '%H:%M:%S').time()

        return latest_time or datetime.min.time()

    sorted_attendances = sorted(attendances, key=custom_sort, reverse=True)

    data = [
        {
            'name': get_employee_name(attendance.EmpCode_id),
            'timein': str(attendance.timein),
            'breakout': str(attendance.breakout),
            'breakin': str(attendance.breakin),
            'timeout': str(attendance.timeout),
            'absent': str(attendance.absent)
        } for attendance in sorted_attendances
    ]

    return JsonResponse({'attendances': data})


def get_employee_name(emp_code):
    try:
        employee = Employee.objects.get(EmpCode=emp_code)
        return f"{employee.Firstname} {employee.Middlename} {employee.Lastname}"
    except Employee.DoesNotExist:
        return "Unknown Employee"

# Responsible for updating the count of total employee
def employee_count(request):
    current_date = date.today()

    
    timed_out_employees = DailyRecord.objects.filter(date=current_date, timeout__isnull=False).count()

    total_employees = DailyRecord.objects.filter(date=current_date).count()

    total_employees_count = total_employees - timed_out_employees

    data = {'total_employees_count': total_employees_count}
    return JsonResponse(data)


# responsible for updating the count for late employee
def employee_late(request):
    current_date = date.today()
    current_time = datetime.now().time()

    late_threshold = time(7, 0, 0)  

    late_employees = DailyRecord.objects.filter(
        date=current_date,
        timein__gt=late_threshold
    ).count()


    data = {'late_employees': late_employees}
    return JsonResponse(data)

# responsible for updating early employees count
def employee_early(request):
    current_date = date.today()
    current_time = datetime.now().time()

    early_threshold = time(7, 0, 0)

    early_employees = DailyRecord.objects.filter(
        date=current_date,
        timein__lt=early_threshold
    ).count()

    data = {'early_employees': early_employees}
    return JsonResponse(data)


