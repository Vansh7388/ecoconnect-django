from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
]