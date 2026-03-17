from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_view, name='dashboard'),
    path('api/check-session/', views.check_session, name='check-session'),
    path('api/extend-session/', views.extend_session, name='extend-session'),
    path('settings/', views.settings_view, name='settings'),
    
    # ADMIN MENU - USER MANAGEMENT
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/groups/', views.admin_groups, name='admin_groups'),
    path('admin/permissions/', views.admin_permissions, name='admin_permissions'),
    path('admin/login-logs/', views.admin_login_logs, name='admin_login_logs'),
    
    # ADMIN MENU - COMPANY SETTINGS
    path('admin/company-profile/', views.admin_company_profile, name='admin_company_profile'),
    path('admin/fiscal-year/', views.admin_fiscal_year, name='admin_fiscal_year'),
    path('admin/system-settings/', views.admin_system_settings, name='admin_system_settings'),
    
    # ADMIN MENU - MODULE CONFIG
    path('admin/modules/', views.admin_modules, name='admin_modules'),
    path('admin/module-settings/', views.admin_module_settings, name='admin_module_settings'),
    path('admin/ui-customization/', views.admin_ui_customization, name='admin_ui_customization'),
    
    # ADMIN MENU - SYSTEM ADMIN
    path('admin/backup/', views.admin_backup, name='admin_backup'),
    path('admin/system-logs/', views.admin_system_logs, name='admin_system_logs'),
    path('admin/cache/', views.admin_cache, name='admin_cache'),
    path('admin/email-config/', views.admin_email_config, name='admin_email_config'),
    
    # ADMIN MENU - AUDIT & COMPLIANCE
    path('admin/audit-trail/', views.admin_audit_trail, name='admin_audit_trail'),
    path('admin/report-templates/', views.admin_report_templates, name='admin_report_templates'),
    path('admin/security-settings/', views.admin_security_settings, name='admin_security_settings'),
]