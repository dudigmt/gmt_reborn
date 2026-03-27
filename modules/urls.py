from django.urls import path
from . import views

urlpatterns = [
    path('module-settings/', views.module_settings, name='module_settings'),
]