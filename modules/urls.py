from django.urls import path
from . import views

urlpatterns = [
    path('module-settings/', views.module_settings, name='module_settings'),
    path('module-settings/add/', views.add_module, name='add_module'),
    path('module-settings/<str:module_name>/edit/', views.edit_module, name='edit_module'),
    path('module-settings/<str:module_name>/delete/', views.delete_module, name='delete_module'),
    path('module-settings/<str:module_name>/add/', views.add_submodule, name='add_submodule'),
    path('module-settings/<str:module_name>/<str:submodule_name>/edit/', views.edit_submodule, name='edit_submodule'),
    path('module-settings/<str:module_name>/<str:submodule_name>/delete/', views.delete_submodule, name='delete_submodule'),
]