from datetime import datetime,date
from django.shortcuts import render, redirect
import openpyxl
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from .forms import  DailyActivityReportForm
from .models import DailyActivityReport, CustomUser , Department
from django.contrib.auth.decorators import login_required , user_passes_test
from  django.contrib import messages
from django.contrib.auth.models import User



def home(request):
    return render(request, 'users/login.html')

def create_user(request):
    return render(request, 'users/create_user.html' )

# Login Page 
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
       
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print(f"Authenticated user: {user.username}")
            auth_login(request, user)
            
           
            if user.is_superuser:
                print("User is superuser (admin)")
                return redirect('users:admin_dashboard')  
            else:
                print("User is not admin")
                return redirect('users:daily_activity') 
        else:
            print("Authentication failed.")
            messages.error(request, "Invalid username or password!")
            return render(request, 'users/login.html')

    return render(request, 'users/login.html')

# Admin Dashboard (Add User/Admin page)
@login_required
def admin_dashboard(request):
    action = request.GET.get('action')
    departments = Department.objects.all()

    if request.method == 'POST':
        # Get the form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        department_name = request.POST.get('department')

        # Check if the department exists
        try:
            department = Department.objects.get(name=department_name)
        except Department.DoesNotExist:
            return render(request, 'users/admin_dashboard.html', {
                'action': action,
                'departments': departments,
                'error': f"Department {department_name} does not exist!"
            })

        # Check if the username already exists
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'users/admin_dashboard.html', {
                'action': action,
                'departments': departments,
                'error': f"Username {username} already exists!"
            })

        # Create the user based on the action
        if action == 'add_user':
            user = CustomUser.objects.create_user(username=username, password=password)
            user.save()
            

        elif action == 'add_admin':
            user = CustomUser.objects.create_user(username=username, password=password)
            user.is_staff = True
            user.is_superuser = True
            user.save()

            permissions = request.POST.getlist('permissions')
            if 'can_edit' in permissions:
                user.can_edit = True
            if 'can_delete' in permissions:
                user.can_delete = True
            if 'can_add_admin' in permissions:
                user.can_add_admin = True
            user.save()

        # Redirect to the same page after the operation
        return redirect('users:admin_dashboard')

    return render(request, 'users/admin_dashboard.html', {
        'action': action,
        'departments': departments
    })
   
# User Daily Activity Page
@login_required
def daily_activity(request):
    user = request.user
    today = date.today()

    # If the user doesn't have a daily activity report yet, create one
    try:
        daily_report = DailyActivityReport.objects.get(user=user, date=date.today())
    except DailyActivityReport.DoesNotExist:
        daily_report = None

    if request.method == 'POST':
        form = DailyActivityReportForm(request.POST, instance=daily_report)

        if form.is_valid():
            activity_report = form.save(commit=False)
            activity_report.user = user
            activity_report.save()
            messages.success(request, "Your daily activity report has been updated.")
            return redirect('users:daily_activity')
    else:
        form = DailyActivityReportForm(instance=daily_report)

    return render(request, 'users/daily_activity.html', {'form': form})



