from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_view, name='dashboard'),
    path('api/check-session/', views.check_session, name='check-session'),
    path('api/extend-session/', views.extend_session, name='extend-session'),
    path('settings/', views.settings_view, name='settings'),
    
    # SYSADMIN MENU - SEMUA PAKAI PREFIX 'sysadmin/' (bukan 'admin/')
    # Ini biar ga bentrok dengan Django Admin di /admin/
    path('sysadmin/', views.sysadmin_dashboard, name='sysadmin_dashboard'),
    
    # SYSADMIN MENU - USER MANAGEMENT
    path('sysadmin/users/', views.sysadmin_users, name='sysadmin_users'),
    path('sysadmin/groups/', views.sysadmin_groups, name='sysadmin_groups'),
    path('sysadmin/permissions/', views.sysadmin_permissions, name='sysadmin_permissions'),
    path('sysadmin/login-logs/', views.sysadmin_login_logs, name='sysadmin_login_logs'),
    
    # SYSADMIN MENU - COMPANY SETTINGS
    path('sysadmin/company-profile/', views.sysadmin_company_profile, name='sysadmin_company_profile'),
    path('sysadmin/fiscal-year/', views.sysadmin_fiscal_year, name='sysadmin_fiscal_year'),
    path('sysadmin/system-settings/', views.sysadmin_system_settings, name='sysadmin_system_settings'),
    
    # SYSADMIN MENU - MODULE CONFIG
    path('sysadmin/modules/', views.sysadmin_modules, name='sysadmin_modules'),
    path('sysadmin/module-settings/', views.sysadmin_module_settings, name='sysadmin_module_settings'),
    path('sysadmin/ui-customization/', views.sysadmin_ui_customization, name='sysadmin_ui_customization'),
    
    # SYSADMIN MENU - SYSTEM ADMIN
    path('sysadmin/backup/', views.sysadmin_backup, name='sysadmin_backup'),
    path('sysadmin/system-logs/', views.sysadmin_system_logs, name='sysadmin_system_logs'),
    path('sysadmin/cache/', views.sysadmin_cache, name='sysadmin_cache'),
    path('sysadmin/email-config/', views.sysadmin_email_config, name='sysadmin_email_config'),
    
    # SYSADMIN MENU - AUDIT & COMPLIANCE
    path('sysadmin/audit-trail/', views.sysadmin_audit_trail, name='sysadmin_audit_trail'),
    path('sysadmin/report-templates/', views.sysadmin_report_templates, name='sysadmin_report_templates'),
    path('sysadmin/security-settings/', views.sysadmin_security_settings, name='sysadmin_security_settings'),
]