from django.contrib import admin
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Section, Dept, Division, Jabatan, Employee, Agama, Pendidikan, StatusKaryawan, PosisiKaryawan

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
    
    class Media:
        js = ('admin/js/employee_filter.js',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama', 'dept', 'is_active']
    list_filter = ['dept']
    search_fields = ['kode', 'nama']

@admin.register(Dept)
class DeptAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama', 'division', 'is_active']
    search_fields = ['kode', 'nama']

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama', 'is_active']

@admin.register(Jabatan)
class JabatanAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama', 'level', 'tugas_utama', 'is_active']
    list_filter = ['dept', 'level']
    search_fields = ['kode', 'nama']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm
    list_display = ['nik', 'nama', 'division', 'dept', 'section', 'jabatan', 'status_karyawan', 'status_kerja']
    list_filter = ['division', 'dept', 'section', 'jabatan', 'status_karyawan', 'status_kerja']
    search_fields = ['nik', 'nama']
    exclude = ['created_by']

    class Media:
        js = ('admin/js/employee_filter.js',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Agama)
class AgamaAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama', 'is_active']

@admin.register(Pendidikan)
class PendidikanAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama', 'urutan', 'is_active']

@admin.register(StatusKaryawan)
class StatusKaryawanAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama', 'is_active']

@admin.register(PosisiKaryawan)
class PosisiKaryawanAdmin(admin.ModelAdmin):
    list_display = ['kode', 'nama', 'is_active']