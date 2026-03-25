from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import LoginHistory
from .models import CompanyProfile

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
    active_tab = request.GET.get('tab', 'users')
    return render(request, 'sysadmin_dashboard.html', {'active_tab': active_tab})

# ===== USER MANAGEMENT =====
@staff_member_required
def sysadmin_users(request):
    if not request.user.is_staff:
        return redirect('/')
    
    query = request.GET.get('q', '')
    users_list = User.objects.all().order_by('-date_joined')
    if query:
        users_list = users_list.filter(Q(username__icontains=query) | Q(email__icontains=query))
    
    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    return render(request, 'sysadmin_users.html', {'users': users})

def sysadmin_users_add(request):
    if not request.user.is_staff:
        return redirect('/')
    
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
            return render(request, 'sysadmin_users_add.html', {'errors': errors})
        
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password1),
            is_staff=is_staff,
            is_active=is_active
        )
        return redirect('sysadmin_users')
    
    return render(request, 'sysadmin_users_add.html')

def sysadmin_users_edit(request, user_id):
    if not request.user.is_staff:
        return redirect('/')
    
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
    
    return render(request, 'sysadmin_users_edit.html', {'user': user})

def sysadmin_users_delete(request, user_id):
    if not request.user.is_staff:
        return redirect('/')
    
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user != request.user:  # Prevent self-deletion
            user.delete()
        return redirect('sysadmin_users')
    
    return redirect('sysadmin_users')

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

def hr_dashboard(request):
    return render(request, 'hr_dashboard.html')

def finance_dashboard(request):
    return render(request, 'finance_dashboard.html')

def production_dashboard(request):
    return render(request, 'production_dashboard.html')

def warehouse_dashboard(request):
    return render(request, 'warehouse_dashboard.html')


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
    
    return render(request, 'login.html', {'expired_time': expired_time})


def sysadmin_company(request):
    if not request.user.is_staff:
        return redirect('/')
    
    profile = CompanyProfile.get_profile()
    
    if request.method == 'POST':
        profile.name = request.POST.get('name', 'GMT Reborn')
        profile.address = request.POST.get('address', '')
        profile.phone = request.POST.get('phone', '')
        profile.email = request.POST.get('email', '')
        profile.tax_id = request.POST.get('tax_id', '')
        profile.currency = request.POST.get('currency', 'IDR')
        profile.date_format = request.POST.get('date_format', 'd/m/Y')
        
        # Handle logo upload
        if request.FILES.get('logo'):
            profile.logo = request.FILES['logo']
        
        profile.updated_by = request.user
        profile.save()
        
        return redirect('sysadmin_company')
    
    return render(request, 'admin/company.html', {'profile': profile})