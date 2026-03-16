from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_view, name='dashboard'),
    path('api/check-session/', views.check_session, name='check-session'),
    path('api/extend-session/', views.extend_session, name='extend-session'),
]