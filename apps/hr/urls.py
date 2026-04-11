from django.urls import path
from . import views

urlpatterns = [
    path('api/dept-by-division/', views.get_dept_by_division, name='get_dept_by_division'),
    path('api/section-by-dept/', views.get_section_by_dept, name='get_section_by_dept'),
    path('api/jabatan-by-dept/', views.get_jabatan_by_dept, name='get_jabatan_by_dept'),
]