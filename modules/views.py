from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Module

@staff_member_required
def module_settings(request):
    modules = Module.objects.all().order_by('order')
    
    if request.method == 'POST':
        for module in modules:
            enabled = request.POST.get(f'module_{module.name}') == 'on'
            if module.is_enabled != enabled:
                module.is_enabled = enabled
                module.save()
        
        messages.success(request, 'Module settings updated successfully')
        return redirect('module_settings')
    
    context = {
        'modules': modules,
        'active_tab': 'modules'
    }
    return render(request, 'sysadmin_modules.html', context)