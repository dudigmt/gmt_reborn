from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_view, name='dashboard'),
    path('api/check-session/', views.check_session, name='check-session'),
    path('api/extend-session/', views.extend_session, name='extend-session'),
    path('settings/', views.settings_view, name='settings'),
    
    # Module Dashboards
    path('hr/', views.hr_dashboard, name='hr_dashboard'),
    path('finance/', views.finance_dashboard, name='finance_dashboard'),
    path('production/', views.production_dashboard, name='production_dashboard'),
    path('warehouse/', views.warehouse_dashboard, name='warehouse_dashboard'),
    
    # ===== SYSADMIN - USER MANAGEMENT =====
    path('sysadmin/users/', views.sysadmin_users, name='sysadmin_users'),
    path('sysadmin/users/add/', views.sysadmin_users_add, name='sysadmin_users_add'),
    path('sysadmin/users/<int:user_id>/edit/', views.sysadmin_users_edit, name='sysadmin_users_edit'),
    path('sysadmin/users/<int:user_id>/delete/', views.sysadmin_users_delete, name='sysadmin_users_delete'),
    
    # ===== SYSADMIN - COMPANY SETTINGS =====
    path('sysadmin/company/', views.sysadmin_company, name='sysadmin_company'),
    
    # ===== SYSADMIN - MODULES, SYSTEM, AUDIT (DUMMY) =====
    path('sysadmin/modules/', views.sysadmin_modules, name='sysadmin_modules'),
    path('sysadmin/system/', views.sysadmin_system, name='sysadmin_system'),
    path('sysadmin/audit/', views.sysadmin_audit, name='sysadmin_audit'),
]