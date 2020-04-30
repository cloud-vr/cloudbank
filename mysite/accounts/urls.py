from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('user_list', views.UserList.as_view(), name='user_list'),
    path('create_user', views.UserCreate.as_view(), name='create_user'),
    path('update_user/<int:pk>/', views.UserUpdate.as_view(), name='update_user'),
    path('delete_user/<int:pk>/', views.UserDelete.as_view(), name='delete_user'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout')
]
