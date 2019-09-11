from django.urls import path
from user import views

urlpatterns = [

    # user routes
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
