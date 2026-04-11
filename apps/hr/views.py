from django.http import JsonResponse
from django.db import models
from .models import Dept, Jabatan, Section

def get_dept_by_division(request):
    division_id = request.GET.get('division_id')
    if division_id:
        depts = Dept.objects.filter(division_id=division_id, is_active=True).values('id', 'nama')
        return JsonResponse(list(depts), safe=False)
    return JsonResponse([], safe=False)

def get_section_by_dept(request):
    dept_id = request.GET.get('dept_id')
    if dept_id:
        sections = Section.objects.filter(dept_id=dept_id, is_active=True).values('id', 'nama')
        return JsonResponse(list(sections), safe=False)
    return JsonResponse([], safe=False)

def get_jabatan_by_dept(request):
    dept_id = request.GET.get('dept_id')
    if dept_id:
        jabatan = Jabatan.objects.filter(models.Q(dept_id=dept_id) | models.Q(dept__isnull=True), is_active=True).values('id', 'nama')
        return JsonResponse(list(jabatan), safe=False)
    return JsonResponse([], safe=False)