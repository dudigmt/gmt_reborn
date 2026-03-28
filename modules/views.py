import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Module
from django.conf import settings
from .icon_choices import ICON_CHOICES

@staff_member_required
def module_settings(request):
    modules = Module.objects.all().order_by('order')
    
    if request.method == 'POST':
        for module in modules:
            # Skip system modules - cannot be disabled
            if module.is_system:
                continue
                
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
        return redirect('sysadmin_modules')
    
    context = {
        'modules': modules,
        'active_tab': 'modules'
    }
    return render(request, 'admin/modules/list.html', context)

@staff_member_required
def edit_submodule(request, module_name, submodule_name):
    module = get_object_or_404(Module, name=module_name)
    submodules = module.submodules
    submodule = None
    
    for sub in submodules:
        if sub.get('name') == submodule_name:
            submodule = sub
            break
    
    if not submodule:
        messages.error(request, 'Submodule not found')
        return redirect('module_settings')
    
    if request.method == 'POST':
        # Update submodule data
        for sub in submodules:
            if sub.get('name') == submodule_name:
                sub['display_name'] = request.POST.get('display_name')
                sub['icon'] = request.POST.get('icon')
                sub['url'] = request.POST.get('url')
                sub['order'] = int(request.POST.get('order', sub.get('order', 0)))
                break
        
        module.submodules = submodules
        module.save()
        messages.success(request, f'Submodule {submodule["display_name"]} updated successfully')
        return redirect('module_settings')
    
    context = {
        'module': module,
        'submodule': submodule,
        'icon_choices': ICON_CHOICES,
        'active_tab': 'modules'
    }
    return render(request, 'admin/modules/submodule_edit.html', context)

@staff_member_required
def add_submodule(request, module_name):
    module = get_object_or_404(Module, name=module_name)
    
    if request.method == 'POST':
        submodules = module.submodules or []
        
        name = request.POST.get('name')
        display_name = request.POST.get('display_name')
        icon = request.POST.get('icon')
        url = request.POST.get('url')
        
        # Auto-detect submodule type based on parent module
        is_admin_module = (module_name == 'admin')
        
        new_submodule = {
            'name': name,
            'display_name': display_name,
            'icon': icon,
            'url': url,
            'order': len(submodules) + 1,
            'is_enabled': True
        }
        
        submodules.append(new_submodule)
        module.submodules = submodules
        module.save()
        
        # Auto-generate for admin module submodules
        if is_admin_module:
            # Generate view
            views_path = os.path.join(settings.BASE_DIR, 'apps/core/views.py')
            with open(views_path, 'r') as f:
                views_content = f.read()
            
            if f'def {name}_view(request):' not in views_content:
                with open(views_path, 'a') as f:
                    f.write(f"""
def {name}_view(request):
    return render(request, 'admin/{name}.html')
""")
            
            # Generate URL pattern
            urls_path = os.path.join(settings.BASE_DIR, 'apps/core/urls.py')
            with open(urls_path, 'r') as f:
                urls_content = f.read()
            
            new_url = f"    path('sysadmin/{name}/', views.{name}_view, name='{name}_view'),\n"
            if new_url not in urls_content:
                urls_content = urls_content.replace(']', new_url + ']')
                with open(urls_path, 'w') as f:
                    f.write(urls_content)
            
            # Generate template
            template_path = os.path.join(settings.BASE_DIR, f'templates/admin/{name}.html')
            template_content = f"""{{% extends 'base_authenticated.html' %}}
{{% load static %}}

{{% block title %}}{display_name}{{% endblock %}}

{{% block content %}}
<div class="container mx-auto">
    <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
            <h2 class="card-title">{display_name}</h2>
            <p>Welcome to {display_name}. This is an auto-generated page.</p>
            <p class="text-gray-500 mt-4">You can customize this template at <code>templates/admin/{name}.html</code></p>
        </div>
    </div>
</div>
{{% endblock %}}
"""
            with open(template_path, 'w') as f:
                f.write(template_content)
            
            # Update URL in database to match generated URL
            for sub in module.submodules:
                if sub.get('name') == name:
                    sub['url'] = f'/sysadmin/{name}/'
                    break
            module.save()
            
            messages.success(request, f'Submodule {display_name} added with auto-generated view, URL, and template!')
        else:
            messages.success(request, f'Submodule {display_name} added successfully')
        
        return redirect('module_settings')
    
    context = {
        'module': module,
        'icon_choices': ICON_CHOICES,
        'active_tab': 'modules'
    }
    return render(request, 'admin/modules/submodule_add.html', context)

@staff_member_required
def delete_submodule(request, module_name, submodule_name):
    module = get_object_or_404(Module, name=module_name)
    submodules = module.submodules
    
    if request.method == 'POST':
        submodules = [sub for sub in submodules if sub.get('name') != submodule_name]
        module.submodules = submodules
        module.save()
        messages.success(request, 'Submodule deleted successfully')
        return redirect('module_settings')
    
    return redirect('module_settings')

@staff_member_required
def edit_module(request, module_name):
    module = get_object_or_404(Module, name=module_name)
    
    if request.method == 'POST':
        module.display_name = request.POST.get('display_name')
        module.icon = request.POST.get('icon')
        module.description = request.POST.get('description')
        module.order = int(request.POST.get('order', module.order))
        module.save()
        
        messages.success(request, f'Module {module.display_name} updated successfully')
        return redirect('module_settings')
    
    context = {
        'module': module,
        'icon_choices': ICON_CHOICES,
        'active_tab': 'modules'
    }
    return render(request, 'admin/modules/edit.html', context)

@staff_member_required
def add_module(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        module_type = request.POST.get('module_type', 'standard')
        
        if Module.objects.filter(name=name).exists():
            messages.error(request, f'Module with name {name} already exists')
            return redirect('add_module')
        
        display_name = request.POST.get('display_name')
        
        # Create module in database
        module = Module.objects.create(
            name=name,
            display_name=display_name,
            icon=request.POST.get('icon'),
            description=request.POST.get('description'),
            order=Module.objects.count() + 1,
            is_enabled=True,
            is_system=False
        )
        
        if module_type == 'standard':
            # Generate standard dashboard view
            views_path = os.path.join(settings.BASE_DIR, 'apps/core/views.py')
            with open(views_path, 'a') as f:
                f.write(f"\ndef {name}_dashboard(request):\n    return render(request, '{name}_dashboard.html')\n")
            
            # Generate URL pattern
            urls_path = os.path.join(settings.BASE_DIR, 'apps/core/urls.py')
            with open(urls_path, 'r') as f:
                urls_content = f.read()
            new_url = f"    path('{name}/', views.{name}_dashboard, name='{name}_dashboard'),\n"
            urls_content = urls_content.replace(']', new_url + ']')
            with open(urls_path, 'w') as f:
                f.write(urls_content)
            
            # Generate template
            template_path = os.path.join(settings.BASE_DIR, f'templates/{name}_dashboard.html')
            template_content = f"""{{% extends 'base_authenticated.html' %}}
{{% load static %}}

{{% block title %}}{display_name} Dashboard{{% endblock %}}

{{% block content %}}
<div class="container mx-auto">
    <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
            <h2 class="card-title">{display_name} Dashboard</h2>
            <p>Welcome to {display_name} module. This is an auto-generated dashboard.</p>
        </div>
    </div>
</div>
{{% endblock %}}
"""
            with open(template_path, 'w') as f:
                f.write(template_content)
                
        else:  # admin module type
            # Generate admin dashboard view
            views_path = os.path.join(settings.BASE_DIR, 'apps/core/views.py')
            with open(views_path, 'a') as f:
                f.write(f"\ndef {name}_dashboard(request):\n    return render(request, 'admin/{name}/dashboard.html')\n")
            
            # Generate URL pattern
            urls_path = os.path.join(settings.BASE_DIR, 'apps/core/urls.py')
            with open(urls_path, 'r') as f:
                urls_content = f.read()
            new_url = f"    path('{name}/', views.{name}_dashboard, name='{name}_dashboard'),\n"
            urls_content = urls_content.replace(']', new_url + ']')
            with open(urls_path, 'w') as f:
                f.write(urls_content)
            
            # Create folder and templates
            os.makedirs(os.path.join(settings.BASE_DIR, f'templates/admin/{name}'), exist_ok=True)
            
            # Dashboard template - using string concatenation to avoid f-string issues
            dashboard_path = os.path.join(settings.BASE_DIR, f'templates/admin/{name}/dashboard.html')
            dashboard_content = '{% extends "base_authenticated.html" %}\n'
            dashboard_content += '{% load static %}\n\n'
            dashboard_content += f'{{% block title %}}{display_name} Dashboard{{% endblock %}}\n\n'
            dashboard_content += '{% block content %}\n'
            dashboard_content += '<div class="container mx-auto">\n'
            dashboard_content += '    <div class="card bg-base-100 shadow-xl">\n'
            dashboard_content += '        <div class="card-body">\n'
            dashboard_content += f'            <h2 class="card-title">{display_name} Dashboard</h2>\n'
            dashboard_content += '            <p>Welcome to this module.</p>\n'
            dashboard_content += '            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">\n'
            dashboard_content += '                {% for submodule in module.submodules %}\n'
            dashboard_content += '                <a href="{{ submodule.url }}" class="btn btn-outline btn-primary">\n'
            dashboard_content += '                    <i class="fa-solid {{ submodule.icon }}"></i>\n'
            dashboard_content += '                    {{ submodule.display_name }}\n'
            dashboard_content += '                </a>\n'
            dashboard_content += '                {% endfor %}\n'
            dashboard_content += '            </div>\n'
            dashboard_content += '        </div>\n'
            dashboard_content += '    </div>\n'
            dashboard_content += '</div>\n'
            dashboard_content += '{% endblock %}'
            
            with open(dashboard_path, 'w') as f:
                f.write(dashboard_content)
            
            # Create default submodules
            submodules = [
                {'name': 'list', 'display_name': 'List', 'icon': 'fa-list', 'url': f'/{name}/list/', 'order': 1, 'is_enabled': True},
                {'name': 'add', 'display_name': 'Add', 'icon': 'fa-plus', 'url': f'/{name}/add/', 'order': 2, 'is_enabled': True},
            ]
            module.submodules = submodules
            module.save()
        
        messages.success(request, f'Module {display_name} created successfully')
        return redirect('module_settings')
    
    context = {
        'icon_choices': ICON_CHOICES,
        'active_tab': 'modules'
    }
    return render(request, 'admin/modules/add.html', context)

@staff_member_required
def delete_module(request, module_name):
    module = get_object_or_404(Module, name=module_name)
    
    # Prevent deletion of system modules
    if module.is_system:
        messages.error(request, f'Cannot delete system module: {module.display_name}')
        return redirect('module_settings')
    
    if request.method == 'POST':
        # 1. Delete template file
        template_path = os.path.join(settings.BASE_DIR, f'templates/{module_name}_dashboard.html')
        if os.path.exists(template_path):
            os.remove(template_path)
        
        # 2. Remove view function from core/views.py
        views_path = os.path.join(settings.BASE_DIR, 'apps/core/views.py')
        with open(views_path, 'r') as f:
            views_lines = f.readlines()
        
        # Find and remove the view function
        new_views_lines = []
        skip = False
        for line in views_lines:
            if f'def {module_name}_dashboard(request):' in line:
                skip = True
                continue
            if skip and line.strip() == '':
                skip = False
                continue
            if not skip:
                new_views_lines.append(line)
        
        with open(views_path, 'w') as f:
            f.writelines(new_views_lines)
        
        # 3. Remove URL pattern from core/urls.py
        urls_path = os.path.join(settings.BASE_DIR, 'apps/core/urls.py')
        with open(urls_path, 'r') as f:
            urls_lines = f.readlines()
        
        new_urls_lines = []
        for line in urls_lines:
            if f"path('{module_name}/'" not in line:
                new_urls_lines.append(line)
        
        with open(urls_path, 'w') as f:
            f.writelines(new_urls_lines)
        
        # 4. Delete module from database
        module_name_display = module.display_name
        module.delete()
        
        messages.success(request, f'Module {module_name_display} and all related files deleted successfully')
        return redirect('module_settings')
    
    context = {
        'module': module,
        'active_tab': 'modules'
    }
    return render(request, 'admin/modules/delete.html', context)

@staff_member_required
def reorder_modules(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for module_name, order in data.items():
                module = Module.objects.get(name=module_name)
                module.order = order
                module.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)