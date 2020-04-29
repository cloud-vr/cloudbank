from django.urls import path

from . import views

app_name = 'bank'

urlpatterns = [
    path('application_list', views.application_list, name='application_list'),
    path('client_list', views.ClientList.as_view(), name='client_list'),
    path('create_client', views.ClientCreate.as_view(), name='create_client'),
    path('update_client/<int:pk>/', views.ClientUpdate.as_view(), name='update_client'),
    path('deposit_trx_list', views.DepositTransactionList.as_view(), name='deposit_trx_list'),
    path('create_deposit_trx', views.DepositCreate.as_view(), name='create_deposit_trx'),
    path('withdraw_trx_list', views.WithdrawTransactionList.as_view(), name='withdraw_trx_list'),
    path('create_withdraw_trx', views.WithdrawCreate.as_view(), name='create_withdraw_trx'),
    path('transfer_trx_list', views.TransferTransactionList.as_view(), name='transfer_trx_list'),
    path('create_transfer_trx', views.TransferCreate.as_view(), name='create_transfer_trx')
]
