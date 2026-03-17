from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

def login_view(request):
    expired_time = None
    
    if request.GET.get('expired'):
        from django.utils import timezone
        import datetime
        now = timezone.localtime(timezone.now())
        expired_time = now.strftime('%d %B %Y, %H:%M:%S')
        print('EXPIRED:', expired_time)  # Buat debug
    
    if request.method == 'POST':
        from django.contrib.auth import authenticate, login
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('/')
    
    return render(request, 'login.html', {'expired_time': expired_time})

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

def settings_view(request):
    from .models import GMTSettings  # IMPORT DI DALAM FUNGSI
    from django.contrib import messages
    
    settings = GMTSettings.get_settings()
    
    if request.method == 'POST':
        session_timeout = request.POST.get('session_timeout')
        if session_timeout and session_timeout.isdigit():
            settings.session_timeout = int(session_timeout)
            settings.updated_by = request.user
            settings.save()
            messages.success(request, 'Settings updated successfully')
        else:
            messages.error(request, 'Invalid session timeout value')
    
    return render(request, 'settings.html', {'settings': settings})

# ===== SYSADMIN DASHBOARD =====
def sysadmin_dashboard(request):
    if not request.user.is_staff:
        return redirect('/')
    return render(request, 'admin_dashboard.html', {'active_tab': 'users'})

# ===== USER MANAGEMENT =====
@staff_member_required
def sysadmin_users(request):
    return render(request, 'admin_dummy.html', {'title': 'User Management', 'section': 'users'})

@staff_member_required
def sysadmin_groups(request):
    return render(request, 'admin_dummy.html', {'title': 'Groups', 'section': 'groups'})

@staff_member_required
def sysadmin_permissions(request):
    return render(request, 'admin_dummy.html', {'title': 'Permissions', 'section': 'permissions'})

@staff_member_required
def sysadmin_login_logs(request):
    return render(request, 'admin_dummy.html', {'title': 'Login Logs', 'section': 'login_logs'})

# ===== COMPANY SETTINGS =====
@staff_member_required
def sysadmin_company_profile(request):
    return render(request, 'admin_dummy.html', {'title': 'Company Profile', 'section': 'company_profile'})

@staff_member_required
def sysadmin_fiscal_year(request):
    return render(request, 'admin_dummy.html', {'title': 'Fiscal Year', 'section': 'fiscal_year'})

@staff_member_required
def sysadmin_system_settings(request):
    return render(request, 'admin_dummy.html', {'title': 'System Settings', 'section': 'system_settings'})

# ===== MODULE CONFIG =====
@staff_member_required
def sysadmin_modules(request):
    return render(request, 'admin_dummy.html', {'title': 'Module Management', 'section': 'modules'})

@staff_member_required
def sysadmin_module_settings(request):
    return render(request, 'admin_dummy.html', {'title': 'Module Settings', 'section': 'module_settings'})

@staff_member_required
def sysadmin_ui_customization(request):
    return render(request, 'admin_dummy.html', {'title': 'UI Customization', 'section': 'ui_customization'})

# ===== SYSTEM ADMIN =====
@staff_member_required
def sysadmin_backup(request):
    return render(request, 'admin_dummy.html', {'title': 'Database Backup', 'section': 'backup'})

@staff_member_required
def sysadmin_system_logs(request):
    return render(request, 'admin_dummy.html', {'title': 'System Logs', 'section': 'system_logs'})

@staff_member_required
def sysadmin_cache(request):
    return render(request, 'admin_dummy.html', {'title': 'Cache Management', 'section': 'cache'})

@staff_member_required
def sysadmin_email_config(request):
    return render(request, 'admin_dummy.html', {'title': 'Email Configuration', 'section': 'email_config'})

# ===== AUDIT & COMPLIANCE =====
@staff_member_required
def sysadmin_audit_trail(request):
    return render(request, 'admin_dummy.html', {'title': 'Audit Trail', 'section': 'audit_trail'})

@staff_member_required
def sysadmin_report_templates(request):
    return render(request, 'admin_dummy.html', {'title': 'Report Templates', 'section': 'report_templates'})

@staff_member_required
def sysadmin_security_settings(request):
    return render(request, 'admin_dummy.html', {'title': 'Security Settings', 'section': 'security_settings'})