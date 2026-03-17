from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse

def login_view(request):
    # Cek apakah ini redirect karena session expired
    expired = request.GET.get('expired', False)
    expired_time = None
    
    if expired:
        # Ambil waktu expired dari session (kalo ada)
        expired_time = request.session.get('expired_time', timezone.now())
        # Format waktu
        expired_time = expired_time.strftime('%d %B %Y, %H:%M:%S')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password')
    
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