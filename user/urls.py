from django.urls import path
from user import views

urlpatterns = [

    # user routes
    path('', views.HomeView.as_view(), name='home'),
    path('user/new/', views.UserView.as_view(), name='new_user'),
    path('user/create/', views.UserView.as_view(), name='create_user'),
    path('user/view/', views.ViewUser.as_view(), name='view_user'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
