from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.custom_login, name='login'),
    # path('login/', views.custom_login, name='login'),
    # path('user_login/', views.user_login, name='user_login'),
    path('daily_activity/', views.daily_activity, name='daily_activity'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
 