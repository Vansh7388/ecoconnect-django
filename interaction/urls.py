from django.urls import path
from . import views

app_name = 'interaction'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_photo, name='upload_photo'),
]