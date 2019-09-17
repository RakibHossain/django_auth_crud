from django.urls import path
from user import views

urlpatterns = [

    # user routes
    path('', views.HomeView.as_view(), name='home'),
    path('user/new/', views.UserView.as_view(), name='new_user'),
    path('user/create/', views.UserView.as_view(), name='create_user'),
    path('user/view/', views.ViewUser.as_view(), name='view_user'),
    path('user/edit/<int:id>', views.UserEdit.as_view(), name='edit_user'),
    path('user/update/<int:id>', views.UserEdit.as_view(), name='update_user'),
    path('user/delete/', views.UserDelete.as_view(), name='delete_user'),
    path('user/delete/<int:id>', views.UserDelete.as_view(), name='delete_user'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
