from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),
    path('sysadmin/', views.admin_dashboard, name='admin_dashboard'),
    
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
    
    # SYSADMIN - Modules
    path('sysadmin/modules/', views.sysadmin_modules, name='sysadmin_modules'),
    
    # SYSADMIN - System & Audit
    path('sysadmin/system/', views.sysadmin_system, name='sysadmin_system'),
    path('sysadmin/audit/', views.sysadmin_audit, name='sysadmin_audit'),
    
    # SYSADMIN - Data Manager
    path('sysadmin/data_manager/', views.data_manager_view, name='data_manager_view'),
    path('sysadmin/data_manager/add/', views.data_manager_add, name='data_manager_add'),
    path('sysadmin/data_manager/<str:table_name>/<int:row_id>/edit/', views.data_manager_edit, name='data_manager_edit'),
    path('sysadmin/data_manager/<str:table_name>/<int:row_id>/delete/', views.data_manager_delete, name='data_manager_delete'),
    path('sysadmin/data_manager/<str:table_name>/<int:row_id>/get/', views.data_manager_get_record, name='data_manager_get_record'),
    path('sysadmin/data_manager/table/<str:table_name>/schema/', views.data_manager_get_table_schema, name='data_manager_table_schema'),
    path('sysadmin/data_manager/table/<str:table_name>/edit/', views.data_manager_edit_table, name='data_manager_edit_table'),
    path('sysadmin/data_manager/table/<str:table_name>/delete/', views.data_manager_delete_table, name='data_manager_delete_table'),
    # HAPUS line ini karena function tidak ada:
    # path('sysadmin/data_manager/table/add/', views.data_manager_add_table, name='data_manager_add_table'),
        
    # Invoice
    path('invoice/', views.invoice_dashboard, name='invoice_dashboard'),
]