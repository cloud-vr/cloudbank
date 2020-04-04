from django.urls import path

from . import views

app_name = 'bank'

urlpatterns = [
    path('', views.index, name='index'),
    path('login_page/', views.login_page, name='login'),
    path('login_button/', views.login_button, name='login')
]