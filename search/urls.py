from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.AdvancedSearchView.as_view(), name='advanced_search'),
    path('results/', views.SearchResultsView.as_view(), name='search_results'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
]