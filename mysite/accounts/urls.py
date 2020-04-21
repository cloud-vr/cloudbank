from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('user_list', views.user_list, name='user_list'),
    path('create_user', views.create_user, name='create_user'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout')
]
