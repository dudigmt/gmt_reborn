from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),
    
    # Session API
    path('api/check-session/', views.check_session, name='check-session'),
    path('api/extend-session/', views.extend_session, name='extend-session'),
    
    # Module Dashboards
    path('hr/', views.hr_dashboard, name='hr_dashboard'),
    path('finance/', views.finance_dashboard, name='finance_dashboard'),
    path('production/', views.production_dashboard, name='production_dashboard'),
    path('warehouse/', views.warehouse_dashboard, name='warehouse_dashboard'),
    
    # SYSADMIN - User Management
    path('sysadmin/users/', views.sysadmin_users, name='sysadmin_users'),
    path('sysadmin/users/add/', views.sysadmin_users_add, name='sysadmin_users_add'),
    path('sysadmin/users/<int:user_id>/edit/', views.sysadmin_users_edit, name='sysadmin_users_edit'),
    path('sysadmin/users/<int:user_id>/delete/', views.sysadmin_users_delete, name='sysadmin_users_delete'),
    
    # SYSADMIN - Company Settings
    path('sysadmin/company/', views.sysadmin_company, name='sysadmin_company'),
    
    # SYSADMIN - Modules (redirect ke module_settings)
    path('sysadmin/modules/', views.sysadmin_modules, name='sysadmin_modules'),
    
    # SYSADMIN - System & Audit (coming soon)
    path('sysadmin/system/', views.sysadmin_system, name='sysadmin_system'),
    path('sysadmin/audit/', views.sysadmin_audit, name='sysadmin_audit'),
    path('marketing/', views.marketing_dashboard, name='marketing_dashboard'),
]