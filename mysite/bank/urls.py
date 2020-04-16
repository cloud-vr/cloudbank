from django.urls import path

from . import views

app_name = 'bank'

urlpatterns = [
    path('application_list', views.application_list, name='application_list'),
    path('create_client', views.create_client, name='create_client'),
    path('create_deposit_trx', views.create_deposit_trx, name='create_deposit_trx'),
    path('create_withdraw_trx', views.create_withdraw_trx, name='create_withdraw_trx')
]
