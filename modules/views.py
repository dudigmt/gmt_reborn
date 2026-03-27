from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Module

@staff_member_required
def module_settings(request):
    modules = Module.objects.all().order_by('order')
    
    if request.method == 'POST':
        for module in modules:
            # Handle main module status
            enabled = request.POST.get(f'module_{module.name}') == 'on'
            if module.is_enabled != enabled:
                module.is_enabled = enabled
            
            # Handle submodules status
            submodules = module.submodules
            if submodules:
                updated = False
                for sub in submodules:
                    sub_enabled = request.POST.get(f'submodule_{module.name}_{sub["name"]}') == 'on'
                    if sub.get('is_enabled') != sub_enabled:
                        sub['is_enabled'] = sub_enabled
                        updated = True
                if updated:
                    module.submodules = submodules
            
            module.save()
        
        messages.success(request, 'Module settings updated successfully')
        return redirect('module_settings')
    
    context = {
        'modules': modules,
        'active_tab': 'modules'
    }
    return render(request, 'sysadmin_modules.html', context)