from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse

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