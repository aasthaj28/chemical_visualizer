"""
URL patterns for the API.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health_check'),
    
    # Authentication
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    
    # Data operations
    path('upload/', views.upload_csv, name='upload_csv'),
    path('summary/<int:dataset_id>/', views.get_summary, name='get_summary'),
    path('history/', views.get_history, name='get_history'),
    path('report/<int:dataset_id>/', views.generate_report, name='generate_report'),
]

