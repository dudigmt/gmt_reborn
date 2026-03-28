from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Q
from .models import LoginHistory, CompanyProfile 
from django.conf import settings


def login_view(request):
    expired_time = None
    
    if request.GET.get('expired'):
        now = timezone.localtime(timezone.now())
        expired_time = now.strftime('%d %B %Y, %H:%M:%S')
    
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            
            # Simpan login history
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            LoginHistory.objects.create(
                user=user,
                ip_address=ip,
                user_agent=user_agent
            )
            
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'auth/login.html', {'expired_time': expired_time})


def logout_view(request):
    logout(request)
    return redirect('login')


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'dashboard.html')


def check_session(request):
    if request.user.is_authenticated:
        return HttpResponse('OK')
    return HttpResponse('Unauthorized', status=401)


def extend_session(request):
    if request.user.is_authenticated:
        request.session.set_expiry(1800)  # 30 minutes
        return HttpResponse('OK')
    return HttpResponse('Unauthorized', status=401)

def admin_dashboard(request):
    from django.contrib.auth.models import User
    from django.utils import timezone
    from datetime import timedelta
    from modules.models import Module
    import os
    import psutil
    
    total_users = User.objects.count()
    total_modules = Module.objects.count()
    today_logins = 0  # nanti diisi dari LoginHistory
    
    # DB size (approximate)
    db_size = "N/A"
    try:
        import subprocess
        result = subprocess.run(['du', '-sh', '/home/adung/projects/gmt_reborn'], capture_output=True, text=True)
        db_size = result.stdout.split()[0] if result.returncode == 0 else "N/A"
    except:
        pass
    
    # Uptime
    uptime = "N/A"
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            uptime = f"{hours}h {minutes}m"
    except:
        pass
    
    # Recent logs placeholder
    recent_logs = []
    
    context = {
        'total_users': total_users,
        'total_modules': total_modules,
        'today_logins': today_logins,
        'db_size': db_size,
        'uptime': uptime,
        'recent_logs': recent_logs,
    }
    return render(request, 'admin/dashboard.html', context)

#def settings_view(request):
#    settings = GMTSettings.get_settings()
#    
#    if request.method == 'POST':
#        session_timeout = request.POST.get('session_timeout')
#        if session_timeout and session_timeout.isdigit():
#            settings.session_timeout = int(session_timeout)
#            settings.updated_by = request.user
#            settings.save()
#            messages.success(request, 'Settings updated successfully')
#        else:
#            messages.error(request, 'Invalid session timeout value')
#    
#    return render(request, 'settings.html', {'settings': settings})


# ===== MODULE DASHBOARDS =====
def hr_dashboard(request):
    return render(request, 'modules/hr_dashboard.html')


def finance_dashboard(request):
    return render(request, 'modules/finance_dashboard.html')


def production_dashboard(request):
    return render(request, 'modules/production_dashboard.html')


def warehouse_dashboard(request):
    return render(request, 'modules/warehouse_dashboard.html')


# ===== SYSADMIN - USER MANAGEMENT =====
@staff_member_required
def sysadmin_users(request):
    query = request.GET.get('q', '')
    users_list = User.objects.all().order_by('-date_joined')
    if query:
        users_list = users_list.filter(Q(username__icontains=query) | Q(email__icontains=query))
    
    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    return render(request, 'admin/users/list.html', {'users': users})


@staff_member_required
def sysadmin_users_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        is_staff = request.POST.get('is_staff') == 'on'
        is_active = request.POST.get('is_active') == 'on'
        
        errors = []
        if not username:
            errors.append('Username is required')
        if not password1 or not password2:
            errors.append('Password is required')
        elif password1 != password2:
            errors.append('Passwords do not match')
        if User.objects.filter(username=username).exists():
            errors.append('Username already exists')
        
        if errors:
            return render(request, 'admin/users/add.html', {'errors': errors})
        
        User.objects.create(
            username=username,
            email=email,
            password=make_password(password1),
            is_staff=is_staff,
            is_active=is_active
        )
        return redirect('sysadmin_users')
    
    return render(request, 'admin/users/add.html')


@staff_member_required
def sysadmin_users_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.is_staff = request.POST.get('is_staff') == 'on'
        user.is_active = request.POST.get('is_active') == 'on'
        
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password1 == password2:
            user.password = make_password(password1)
        
        user.save()
        return redirect('sysadmin_users')
    
    return render(request, 'admin/users/edit.html', {'user': user})


@staff_member_required
def sysadmin_users_delete(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user != request.user:  # Prevent self-deletion
            user.delete()
        return redirect('sysadmin_users')
    
    return redirect('sysadmin_users')


# ===== SYSADMIN - COMPANY SETTINGS =====
@staff_member_required
def sysadmin_company(request):
    profile = CompanyProfile.get_profile()
    
    if request.method == 'POST':
        profile.name = request.POST.get('name', 'GMT Reborn')
        profile.address = request.POST.get('address', '')
        profile.phone = request.POST.get('phone', '')
        profile.email = request.POST.get('email', '')
        profile.tax_id = request.POST.get('tax_id', '')
        profile.currency = request.POST.get('currency', 'IDR')
        profile.date_format = request.POST.get('date_format', 'd/m/Y')
        
        if request.FILES.get('logo'):
            profile.logo = request.FILES['logo']
        
        profile.updated_by = request.user
        profile.save()
        
        return redirect('sysadmin_company')
    
    return render(request, 'admin/company/settings.html', {'profile': profile})


# ===== SYSADMIN - MODULES =====
@staff_member_required
def sysadmin_modules(request):
    from modules.models import Module
    modules = Module.objects.all().order_by('order')
    return render(request, 'admin/modules/list.html', {'modules': modules})


# ===== SYSADMIN - SYSTEM (DUMMY) =====
@staff_member_required
def sysadmin_system(request):
    return render(request, 'admin/system/sysadmin_system.html')


# ===== SYSADMIN - AUDIT (DUMMY) =====
@staff_member_required
def sysadmin_audit(request):
    return render(request, 'admin/audit/logs.html')

import platform
import sys
import django
from django.db import connection
import psutil
from datetime import datetime
import os

@staff_member_required
def sysadmin_system(request):
    # System Info
    system_info = {
        'django_version': django.get_version(),
        'python_version': sys.version.split()[0],
        'database': connection.vendor,
        'database_name': connection.settings_dict['NAME'],
        'os': platform.system(),
        'os_release': platform.release(),
        'hostname': platform.node(),
        'server_time': datetime.now().strftime('%d %B %Y, %H:%M:%S'),
        'environment': 'Development' if settings.DEBUG else 'Production',
    }
    
    # Disk usage
    try:
        disk = psutil.disk_usage('/')
        system_info['disk_total'] = f"{disk.total / (1024**3):.1f} GB"
        system_info['disk_used'] = f"{disk.used / (1024**3):.1f} GB"
        system_info['disk_free'] = f"{disk.free / (1024**3):.1f} GB"
        system_info['disk_percent'] = disk.percent
    except:
        system_info['disk_total'] = 'N/A'
        system_info['disk_used'] = 'N/A'
        system_info['disk_free'] = 'N/A'
        system_info['disk_percent'] = 'N/A'
    
    # Memory usage
    try:
        memory = psutil.virtual_memory()
        system_info['memory_total'] = f"{memory.total / (1024**3):.1f} GB"
        system_info['memory_used'] = f"{memory.used / (1024**3):.1f} GB"
        system_info['memory_percent'] = memory.percent
    except:
        system_info['memory_total'] = 'N/A'
        system_info['memory_used'] = 'N/A'
        system_info['memory_percent'] = 'N/A'
    
    return render(request, 'admin/system/info.html', {'system_info': system_info, 'active_tab': 'system'})