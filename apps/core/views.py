from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import connection
from django.conf import settings
from .models import *
from modules.models import Module
import json
import re
import os


# ============================================================================
# AUTH VIEWS
# ============================================================================

def login_view(request):
    expired_time = None
    
    if request.GET.get('expired'):
        now = timezone.localtime(timezone.now())
        expired_time = now.strftime('%d %B %Y, %H:%M:%S')
    
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            
            Loginhistory.objects.create(
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
        request.session.set_expiry(1800)
        return HttpResponse('OK')
    return HttpResponse('Unauthorized', status=401)


# ============================================================================
# MODULE DASHBOARDS
# ============================================================================

def hr_dashboard(request):
    return render(request, 'modules/hr_dashboard.html')


def finance_dashboard(request):
    return render(request, 'modules/finance_dashboard.html')


def production_dashboard(request):
    return render(request, 'modules/production_dashboard.html')


def warehouse_dashboard(request):
    return render(request, 'modules/warehouse_dashboard.html')


def invoice_dashboard(request):
    return render(request, 'invoice_dashboard.html')


# ============================================================================
# HELPER
# ============================================================================

def get_admin_submodules():
    try:
        admin_module = Module.objects.get(name='admin')
        return [sub for sub in admin_module.submodules if sub.get('is_enabled', True)]
    except:
        return []


# ============================================================================
# SYSADMIN - USER MANAGEMENT
# ============================================================================

@staff_member_required
def sysadmin_users(request):
    query = request.GET.get('q', '')
    users_list = User.objects.all().order_by('-date_joined')
    if query:
        users_list = users_list.filter(Q(username__icontains=query) | Q(email__icontains=query))
    
    paginator = Paginator(users_list, 10)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    admin_submodules = get_admin_submodules()
    return render(request, 'admin/users/list.html', {'users': users, 'admin_submodules': admin_submodules})


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
            admin_submodules = get_admin_submodules()
            return render(request, 'admin/users/add.html', {'errors': errors, 'admin_submodules': admin_submodules})
        
        User.objects.create(
            username=username,
            email=email,
            password=make_password(password1),
            is_staff=is_staff,
            is_active=is_active
        )
        return redirect('sysadmin_users')
    
    admin_submodules = get_admin_submodules()
    return render(request, 'admin/users/add.html', {'admin_submodules': admin_submodules})


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
    
    admin_submodules = get_admin_submodules()
    return render(request, 'admin/users/edit.html', {'user': user, 'admin_submodules': admin_submodules})


@staff_member_required
def sysadmin_users_delete(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user != request.user:
            user.delete()
        return redirect('sysadmin_users')
    return redirect('sysadmin_users')


# ============================================================================
# SYSADMIN - COMPANY
# ============================================================================

@staff_member_required
def sysadmin_company(request):
    profile = Companyprofile.get_profile()
    
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
    
    admin_submodules = get_admin_submodules()
    return render(request, 'admin/company/settings.html', {'profile': profile, 'admin_submodules': admin_submodules})


# ============================================================================
# SYSADMIN - MODULES
# ============================================================================

@staff_member_required
def sysadmin_modules(request):
    modules = Module.objects.all().order_by('order')
    admin_submodules = get_admin_submodules()
    return render(request, 'admin/modules/list.html', {'modules': modules, 'admin_submodules': admin_submodules})


# ============================================================================
# SYSADMIN - SYSTEM
# ============================================================================

@staff_member_required
def sysadmin_system(request):
    import platform
    import sys
    import django
    import psutil
    from datetime import datetime
    
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
    
    try:
        memory = psutil.virtual_memory()
        system_info['memory_total'] = f"{memory.total / (1024**3):.1f} GB"
        system_info['memory_used'] = f"{memory.used / (1024**3):.1f} GB"
        system_info['memory_percent'] = memory.percent
    except:
        system_info['memory_total'] = 'N/A'
        system_info['memory_used'] = 'N/A'
        system_info['memory_percent'] = 'N/A'
    
    admin_submodules = get_admin_submodules()
    return render(request, 'admin/system/info.html', {'system_info': system_info, 'admin_submodules': admin_submodules})


# ============================================================================
# SYSADMIN - AUDIT
# ============================================================================

@staff_member_required
def sysadmin_audit(request):
    admin_submodules = get_admin_submodules()
    return render(request, 'admin/audit/logs.html', {'admin_submodules': admin_submodules})


# ============================================================================
# ADMIN DASHBOARD
# ============================================================================

def admin_dashboard(request):
    admin_module = Module.objects.get(name='admin')
    admin_submodules = [sub for sub in admin_module.submodules if sub.get('is_enabled', True)]
    
    total_users = User.objects.count()
    total_modules = Module.objects.count()
    
    context = {
        'total_users': total_users,
        'total_modules': total_modules,
        'admin_submodules': admin_submodules,
    }
    return render(request, 'admin/dashboard.html', context)


# ============================================================================
# DATA MANAGER - VIEW (Pure SQL for viewing only)
# ============================================================================

def data_manager_view(request):
    tables = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename")
        tables = [row[0] for row in cursor.fetchall()]
    
    selected_table = request.GET.get('table', '')
    columns = []
    rows = []
    row_count = 0
    
    if selected_table and selected_table in tables:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{selected_table}' ORDER BY ordinal_position")
            columns = [col[0] for col in cursor.fetchall()]
            cursor.execute(f'SELECT * FROM "{selected_table}" LIMIT 100')
            rows = list(cursor.fetchall())
            cursor.execute(f'SELECT COUNT(*) FROM "{selected_table}"')
            row_count = cursor.fetchone()[0]
        
        # Khusus untuk tabel hr_dept, ganti parent_id jadi nama group_dept
        if selected_table == 'hr_dept' and 'parent_id' in columns:
            # Ambil semua group_dept untuk mapping
            group_map = {}
            with connection.cursor() as cursor:
                cursor.execute('SELECT id, nama FROM hr_group_dept')
                for row in cursor.fetchall():
                    group_map[row[0]] = row[1]
            
            # Cari index kolom parent_id
            parent_idx = columns.index('parent_id')
            
            # Ganti nilai parent_id jadi nama group
            new_rows = []
            for row in rows:
                row_list = list(row)
                parent_val = row_list[parent_idx]
                if parent_val and parent_val in group_map:
                    row_list[parent_idx] = group_map[parent_val]
                elif parent_val:
                    row_list[parent_idx] = f"ID: {parent_val} (not found)"
                else:
                    row_list[parent_idx] = '-'
                new_rows.append(tuple(row_list))
            rows = new_rows
    
    context = {
        'tables': tables,
        'selected_table': selected_table,
        'columns': columns,
        'rows': rows,
        'row_count': row_count,
        'admin_submodules': get_admin_submodules(),
    }
    return render(request, 'admin/data_manager.html', context)


# ============================================================================
# DATA MANAGER - RECORD CRUD (Untuk tabel yang sudah ada Django models)
# ============================================================================

ALLOWED_TABLES = [
    'core_companyprofile',
    'core_loginhistory',
    'modules_module',
    'auth_user',
    'hr_dept',
    'hr_jabatan',
    'hr_group_dept',
    'hr_employee',
]

EXCLUDED_TABLES = [
    'auth_group',
    'auth_group_permissions',
    'auth_permission',
    'django_admin_log',
    'django_content_type',
    'django_migrations',
    'django_session',
]


@staff_member_required
def data_manager_add(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    table_name = request.POST.get('table_name')
    
    if table_name not in ALLOWED_TABLES or table_name in EXCLUDED_TABLES:
        return JsonResponse({'error': 'Table not allowed for add operation'}, status=403)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
            """, [table_name])
            columns = cursor.fetchall()
        
        columns_list = []
        values_list = []
        placeholders = []
        
        for col in columns:
            col_name = col[0]
            if col_name == 'id':
                continue
            
            value = request.POST.get(col_name)
            if value or col[2] == 'YES':
                columns_list.append(col_name)
                placeholders.append('%s')
                values_list.append(value if value else None)
        
        if not columns_list:
            return JsonResponse({'error': 'No valid columns to insert'}, status=400)
        
        insert_sql = f'INSERT INTO "{table_name}" ({", ".join(columns_list)}) VALUES ({", ".join(placeholders)}) RETURNING id'
        with connection.cursor() as cursor:
            cursor.execute(insert_sql, values_list)
            new_id = cursor.fetchone()[0]
        
        return JsonResponse({'success': True, 'message': 'Record added successfully', 'id': new_id})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
def data_manager_edit(request, table_name, row_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if table_name not in ALLOWED_TABLES or table_name in EXCLUDED_TABLES:
        return JsonResponse({'error': 'Table not allowed for edit operation'}, status=403)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
            """, [table_name])
            columns = cursor.fetchall()
        
        update_fields = []
        values = []
        
        for col in columns:
            col_name = col[0]
            if col_name == 'id':
                continue
            
            value = request.POST.get(col_name)
            if value is not None:
                update_fields.append(f'"{col_name}" = %s')
                values.append(value if value else None)
        
        if not update_fields:
            return JsonResponse({'error': 'No fields to update'}, status=400)
        
        values.append(row_id)
        update_sql = f'UPDATE "{table_name}" SET {", ".join(update_fields)} WHERE id = %s'
        
        with connection.cursor() as cursor:
            cursor.execute(update_sql, values)
        
        return JsonResponse({'success': True, 'message': 'Record updated successfully'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
def data_manager_delete(request, table_name, row_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if table_name not in ALLOWED_TABLES or table_name in EXCLUDED_TABLES:
        return JsonResponse({'error': 'Table not allowed for delete operation'}, status=403)
    
    if table_name == 'auth_user':
        with connection.cursor() as cursor:
            cursor.execute('SELECT username, is_superuser FROM auth_user WHERE id = %s', [row_id])
            user = cursor.fetchone()
            if user and (user[1] or request.user.id == row_id):
                return JsonResponse({'error': 'Cannot delete superuser or yourself'}, status=403)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(f'DELETE FROM "{table_name}" WHERE id = %s', [row_id])
        
        return JsonResponse({'success': True, 'message': 'Record deleted successfully'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@staff_member_required
def data_manager_get_record(request, table_name, row_id):
    if table_name not in ALLOWED_TABLES or table_name in EXCLUDED_TABLES:
        return JsonResponse({'error': 'Table not allowed'}, status=403)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
            """, [table_name])
            columns = [col[0] for col in cursor.fetchall()]
            
            cursor.execute(f'SELECT * FROM "{table_name}" WHERE id = %s', [row_id])
            row = cursor.fetchone()
            
            if not row:
                return JsonResponse({'error': 'Record not found'}, status=404)
            
            data = dict(zip(columns, row))
        
        return JsonResponse({'success': True, 'data': data})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@staff_member_required
def data_manager_delete_table(request, table_name):
    """Delete table - ONLY for NON-Django tables (custom tables)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # PROTECT DJANGO SYSTEM TABLES (TIDAK BISA DIHAPUS)
    if table_name.startswith('hr_') or table_name.startswith('core_') or table_name.startswith('auth_') or table_name.startswith('django_') or table_name.startswith('modules_'):
        return JsonResponse({'error': 'Cannot delete Django system table. Use migration instead.'}, status=403)
    
    # Juga proteksi tabel penting lainnya
    PROTECTED_TABLES = [
        'core_companyprofile', 'core_loginhistory', 'modules_module'
    ]
    if table_name in PROTECTED_TABLES:
        return JsonResponse({'error': f'Cannot delete protected table: {table_name}'}, status=403)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE')
        
        return JsonResponse({'success': True, 'message': f'Table "{table_name}" deleted successfully'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@staff_member_required
def data_manager_edit_table(request, table_name):
    """Alter table structure - BISA untuk SEMUA tabel (termasuk Django tables)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        action = request.POST.get('action')
        
        if action == 'rename':
            new_name = request.POST.get('new_name')
            if not new_name or not re.match(r'^[a-z_][a-z0-9_]*$', new_name):
                return JsonResponse({'error': 'Invalid table name'}, status=400)
            
            # Cek apakah ini tabel Django, kasih warning tapi tetap bisa
            is_django_table = table_name.startswith('hr_') or table_name.startswith('core_') or table_name.startswith('auth_') or table_name.startswith('django_') or table_name.startswith('modules_')
            
            with connection.cursor() as cursor:
                cursor.execute(f'ALTER TABLE "{table_name}" RENAME TO "{new_name}"')
            
            message = f'Table renamed to {new_name}'
            if is_django_table:
                message += ' (Note: This is a Django table. You may need to update models.py manually)'
            
            return JsonResponse({'success': True, 'message': message, 'new_name': new_name})
        
        elif action == 'add_column':
            column_name = request.POST.get('column_name')
            column_type = request.POST.get('column_type')
            column_length = request.POST.get('column_length', '')
            nullable = request.POST.get('nullable') == 'true'
            
            if not column_name or not column_type:
                return JsonResponse({'error': 'Column name and type required'}, status=400)
            
            type_map = {
                'varchar': f'VARCHAR({column_length or 255})',
                'text': 'TEXT',
                'integer': 'INTEGER',
                'bigint': 'BIGINT',
                'decimal': f'DECIMAL(15,{column_length or 2})',
                'boolean': 'BOOLEAN',
                'date': 'DATE',
                'datetime': 'TIMESTAMP',
                'json': 'JSONB'
            }
            
            sql_type = type_map.get(column_type, 'VARCHAR(255)')
            null_constraint = '' if nullable else 'NOT NULL'
            
            with connection.cursor() as cursor:
                cursor.execute(f'ALTER TABLE "{table_name}" ADD COLUMN "{column_name}" {sql_type} {null_constraint}'.strip())
            
            return JsonResponse({'success': True, 'message': f'Column {column_name} added'})
        
        elif action == 'modify_column':
            old_name = request.POST.get('old_name')
            new_name = request.POST.get('new_name')
            column_type = request.POST.get('column_type')
            column_length = request.POST.get('column_length', '')
            nullable = request.POST.get('nullable') == 'true'
            
            if not old_name:
                return JsonResponse({'error': 'Column name required'}, status=400)
            
            with connection.cursor() as cursor:
                if new_name and new_name != old_name:
                    cursor.execute(f'ALTER TABLE "{table_name}" RENAME COLUMN "{old_name}" TO "{new_name}"')
                    old_name = new_name
                
                if column_type:
                    type_map = {
                        'varchar': f'VARCHAR({column_length or 255})',
                        'text': 'TEXT',
                        'integer': 'INTEGER USING "{old_name}"::INTEGER',
                        'bigint': 'BIGINT USING "{old_name}"::BIGINT',
                        'decimal': f'DECIMAL(15,{column_length or 2}) USING "{old_name}"::DECIMAL',
                        'boolean': 'BOOLEAN USING "{old_name}"::BOOLEAN',
                        'date': 'DATE USING "{old_name}"::DATE',
                        'datetime': 'TIMESTAMP USING "{old_name}"::TIMESTAMP',
                        'json': 'JSONB USING "{old_name}"::JSONB'
                    }
                    sql_type = type_map.get(column_type, f'VARCHAR({column_length or 255})')
                    cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "{old_name}" TYPE {sql_type}')
                
                if nullable:
                    cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "{old_name}" DROP NOT NULL')
                else:
                    cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "{old_name}" SET NOT NULL')
            
            return JsonResponse({'success': True, 'message': f'Column {old_name} modified'})
        
        elif action == 'drop_column':
            column_name = request.POST.get('column_name')
            if not column_name:
                return JsonResponse({'error': 'Column name required'}, status=400)
            
            with connection.cursor() as cursor:
                cursor.execute(f'ALTER TABLE "{table_name}" DROP COLUMN "{column_name}" CASCADE')
            
            return JsonResponse({'success': True, 'message': f'Column {column_name} dropped'})
        
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@staff_member_required
def data_manager_get_table_schema(request, table_name):
    """Get table schema for editing - BISA untuk SEMUA tabel"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name, data_type, character_maximum_length, is_nullable
                FROM information_schema.columns
                WHERE table_name = %s
                ORDER BY ordinal_position
            """, [table_name])
            
            columns = []
            for row in cursor.fetchall():
                col_type = row[1]
                if col_type == 'character varying':
                    col_type = 'varchar'
                elif col_type == 'timestamp without time zone':
                    col_type = 'datetime'
                elif col_type == 'numeric':
                    col_type = 'decimal'
                    
                columns.append({
                    'name': row[0],
                    'type': col_type,
                    'length': row[2] if row[2] else None,
                    'nullable': row[3] == 'YES'
                })
            
            return JsonResponse({
                'success': True,
                'table_name': table_name,
                'columns': columns,
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': str(e)
        }, status=500)

# ============================================================================
# DJANGO TABLE SYNC - Auto sync database ke models.py + migration
# ============================================================================

import os
import subprocess
from django.apps import apps

def get_table_columns_detailed(table_name):
    """Get detailed column info from database"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                column_name, 
                data_type, 
                character_maximum_length,
                is_nullable,
                column_default,
                udt_name
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, [table_name])
        columns = []
        for col in cursor.fetchall():
            columns.append({
                'name': col[0],
                'data_type': col[1],
                'max_length': col[2],
                'nullable': col[3] == 'YES',
                'default': col[4],
                'udt_name': col[5]
            })
        return columns

def map_db_to_django_field(col):
    """Map database column ke Django model field"""
    col_name = col['name']
    data_type = col['data_type']
    udt_name = col['udt_name']
    max_length = col['max_length']
    nullable = col['nullable']
    
    if col_name == 'id':
        return None
    
    # Base field tanpa kurung dulu
    if data_type == 'integer':
        field = 'models.IntegerField'
    elif data_type == 'bigint':
        field = 'models.BigIntegerField'
    elif data_type == 'character varying' or udt_name == 'varchar':
        length = max_length or 255
        field = f'models.CharField(max_length={length})'
    elif data_type == 'text':
        field = 'models.TextField'
    elif data_type == 'boolean':
        field = 'models.BooleanField(default=False)'
    elif data_type == 'date':
        field = 'models.DateField'
    elif data_type == 'timestamp without time zone' or udt_name == 'timestamp':
        field = 'models.DateTimeField'
    elif data_type == 'numeric' or udt_name == 'numeric':
        field = 'models.DecimalField(max_digits=15, decimal_places=2)'
    elif udt_name == 'jsonb':
        field = 'models.JSONField'
    else:
        field = 'models.TextField'
    
    # Tambah parameter null/blank
    if nullable and col_name not in ['created_at', 'updated_at']:
        # Hapus kurung tutup dulu kalau ada
        if field.endswith(')'):
            field = field[:-1] + ', blank=True, null=True)'
        else:
            field += '(blank=True, null=True)'
    else:
        if not field.endswith(')'):
            field += '()'
    
    return field

def sync_single_table(table_name, app_name):
    """Sync satu tabel ke model Django"""
    if not table_name.startswith(app_name):
        return False, f"Table {table_name} tidak sesuai dengan app {app_name}"
    
    # Get columns dari database
    columns = get_table_columns_detailed(table_name)
    
    # Generate model code
    # Generate class name dari table_name (hr_dept -> HrDept)
    class_name = ''.join(word.capitalize() for word in table_name.split('_')[1:])
    if not class_name:
        class_name = table_name.capitalize()
    
    model_code = f"""from django.db import models
from django.contrib.auth.models import User


class {class_name}(models.Model):
    \"\"\"Auto-synced from database table: {table_name}\"\"\"
"""
    
    for col in columns:
        field_def = map_db_to_django_field(col)
        if field_def:
            model_code += f"    {col['name']} = {field_def}\n"
    
    model_code += f"""
    class Meta:
        db_table = '{table_name}'
        verbose_name = '{table_name}'
        verbose_name_plural = '{table_name}'
    
    def __str__(self):
        return str(self.id)
"""
    
    # Write to models.py
    models_path = os.path.join(settings.BASE_DIR, f'apps/{app_name}/models.py')
    with open(models_path, 'w') as f:
        f.write(model_code)
    
    return True, f"Model {class_name} berhasil di-sync"

def run_migrations_for_app(app_name):
    """Run makemigrations and migrate untuk app tertentu"""
    try:
        # Run makemigrations
        result = subprocess.run(
            ['python', 'manage.py', 'makemigrations', app_name, '--noinput'],
            cwd=settings.BASE_DIR,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return False, result.stderr
        
        # Run migrate
        result = subprocess.run(
            ['python', 'manage.py', 'migrate', app_name, '--noinput'],
            cwd=settings.BASE_DIR,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return False, result.stderr
        
        return True, "Migration berhasil"
    
    except Exception as e:
        return False, str(e)

@staff_member_required
def data_manager_add_table(request):
    """Create new table with auto-generated Django model + migration"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    table_name = request.POST.get('table_name')
    fields_json = request.POST.get('fields')
    app_name = request.POST.get('app_name', 'hr')  # Default ke hr
    
    if not table_name or not fields_json:
        return JsonResponse({'error': 'Table name and fields are required'}, status=400)
    
    # Validate table name
    if not re.match(r'^[a-z_][a-z0-9_]*$', table_name):
        return JsonResponse({'error': 'Table name must be lowercase, start with letter, and contain only letters, numbers, underscores'}, status=400)
    
    if table_name.startswith('django_') or table_name.startswith('auth_'):
        return JsonResponse({'error': 'Cannot create table with system prefix'}, status=403)
    
    # Valid app name
    if app_name not in ['hr', 'finance', 'production', 'warehouse', 'core']:
        app_name = 'hr'
    
    try:
        fields = json.loads(fields_json)
        
        # Build CREATE TABLE SQL
        columns_sql = [
            '"id" BIGSERIAL PRIMARY KEY',
            '"created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            '"updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
            '"created_by" INTEGER NULL',
            '"is_active" BOOLEAN DEFAULT TRUE'
        ]
        
        for field in fields:
            field_name = field['name']
            field_type = field['type']
            field_length = field.get('length', '')
            nullable = field.get('nullable', True)
            
            if not re.match(r'^[a-z_][a-z0-9_]*$', field_name):
                return JsonResponse({'error': f'Invalid field name: {field_name}'}, status=400)
            
            if field_name in ['id', 'created_at', 'updated_at', 'created_by', 'is_active']:
                continue
            
            type_map = {
                'varchar': f'VARCHAR({field_length or 255})',
                'text': 'TEXT',
                'integer': 'INTEGER',
                'bigint': 'BIGINT',
                'decimal': f'DECIMAL(15,{field_length or 2})',
                'boolean': 'BOOLEAN',
                'date': 'DATE',
                'datetime': 'TIMESTAMP',
                'json': 'JSONB'
            }
            
            sql_type = type_map.get(field_type, 'VARCHAR(255)')
            null_constraint = '' if nullable else 'NOT NULL'
            col_def = f'"{field_name}" {sql_type} {null_constraint}'.strip()
            columns_sql.append(col_def)
        
        # Create table
        create_sql = f'CREATE TABLE "{table_name}" (\n    ' + ',\n    '.join(columns_sql) + '\n)'
        
        with connection.cursor() as cursor:
            cursor.execute(create_sql)
            
            # Create trigger for updated_at
            cursor.execute("""
                CREATE OR REPLACE FUNCTION update_updated_at_column()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ language 'plpgsql';
            """)
            
            cursor.execute(f"""
                DROP TRIGGER IF EXISTS update_{table_name}_updated_at ON "{table_name}";
                CREATE TRIGGER update_{table_name}_updated_at
                    BEFORE UPDATE ON "{table_name}"
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at_column();
            """)
        
        # Generate Django model
        success, message = sync_single_table(table_name, app_name)
        if not success:
            return JsonResponse({'error': f'Table created but model sync failed: {message}'}, status=500)
        
        # Auto migration
        from io import StringIO
        from django.core.management import call_command
        
        out = StringIO()
        call_command('makemigrations', app_name, '--noinput', stdout=out, stderr=out)
        call_command('migrate', app_name, '--noinput', stdout=out, stderr=out)
        
        return JsonResponse({
            'success': True,
            'message': f'Table "{table_name}" created with Django model + auto migration!',
            'table_name': table_name
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid fields data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@staff_member_required
def sync_django_table(request, table_name):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Cek apakah perlu sync
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = %s
            )
        """, [table_name])
        if not cursor.fetchone()[0]:
            return JsonResponse({'error': f'Table {table_name} not found'}, status=404)
    
    # Tentukan app name
    if table_name.startswith('hr_'):
        app_name = 'hr'
    elif table_name.startswith('core_'):
        app_name = 'core'
    elif table_name.startswith('modules_'):
        app_name = 'modules'
    else:
        return JsonResponse({'error': f'Unknown app for table: {table_name}'}, status=400)
    
    try:
        # 1. Sync model ke models.py
        success, message = sync_single_table(table_name, app_name)
        if not success:
            return JsonResponse({'error': message}, status=500)
        
        # 2. Auto makemigrations
        from io import StringIO
        from django.core.management import call_command
        
        out = StringIO()
        call_command('makemigrations', app_name, '--noinput', stdout=out, stderr=out)
        
        # 3. Auto migrate
        call_command('migrate', app_name, '--noinput', stdout=out, stderr=out)
        
        return JsonResponse({
            'success': True,
            'message': f'Table {table_name} berhasil disinkronkan + migration otomatis'
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@staff_member_required
def check_table_sync_status(request, table_name):
    """Cek apakah tabel perlu sync"""
    try:
        # Tentukan app name
        if table_name.startswith('hr_'):
            app_name = 'hr'
        elif table_name.startswith('core_'):
            app_name = 'core'
        elif table_name.startswith('modules_'):
            app_name = 'modules'
        else:
            return JsonResponse({'needs_sync': False, 'message': 'Not a Django table'})
        
        # Get columns dari database
        db_columns = get_table_columns_detailed(table_name)
        db_column_names = set([c['name'] for c in db_columns if c['name'] != 'id'])
        
        # Get columns dari model (coba import model)
        try:
            model_module = __import__(f'apps.{app_name}.models', fromlist=[''])
            model_class = getattr(model_module, table_name.split('_')[1].capitalize())
            model_column_names = set([f.name for f in model_class._meta.get_fields() if f.name != 'id'])
        except:
            return JsonResponse({'needs_sync': True, 'message': 'Model tidak ditemukan, perlu sync'})
        
        # Bandingkan
        if db_column_names == model_column_names:
            return JsonResponse({'needs_sync': False, 'message': 'Model dan database sudah sinkron'})
        else:
            added = db_column_names - model_column_names
            removed = model_column_names - db_column_names
            return JsonResponse({
                'needs_sync': True,
                'message': f'Perubahan: +{len(added)} kolom, -{len(removed)} kolom',
                'added_columns': list(added),
                'removed_columns': list(removed)
            })
    
    except Exception as e:
        return JsonResponse({'needs_sync': False, 'message': str(e)})