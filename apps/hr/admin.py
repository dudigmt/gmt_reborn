from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['nik', 'nama', 'dept', 'jabatan', 'status_karyawan', 'status_kerja']
    search_fields = ['nik', 'nama', 'no_ktp']
    list_filter = ['dept', 'status_karyawan', 'status_kerja']