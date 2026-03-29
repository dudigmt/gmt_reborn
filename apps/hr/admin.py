from django.contrib import admin
from .models import Dept, GroupDept, Jabatan, Employee

@admin.register(Dept)
class DeptAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama', 'parent', 'is_active']
    search_fields = ['kode', 'nama']

@admin.register(GroupDept)
class GroupDeptAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama', 'is_active']
    search_fields = ['kode', 'nama']

@admin.register(Jabatan)
class JabatanAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama', 'level', 'is_active']
    search_fields = ['kode', 'nama']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['nik', 'nama', 'dept', 'jabatan']
    list_filter = ['dept', 'jabatan']
    search_fields = ['nik', 'nama']
