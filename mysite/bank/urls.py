from django.urls import path

from . import views

app_name = 'bank'

urlpatterns = [
    path('application_list', views.application_list, name='application_list'),
    path('client_accounts', views.client_accounts, name='client_accounts'),
    path('view_client', views.view_client, name='view_client'),
    path('create_client', views.create_client, name='create_client'),
    path('edit_client', views.edit_client, name='edit_client'),
    path('delete_client', views.delete_client, name='delete_client'),
    path('view_deposit_trx', views.DepositTransactionList.as_view(), name='view_deposit_trx'),
    path('create_deposit_trx', views.create_deposit_trx, name='create_deposit_trx'),
    path('view_withdraw_trx', views.WithdrawTransactionList.as_view(), name='view_withdraw_trx'),
    path('create_withdraw_trx', views.create_withdraw_trx, name='create_withdraw_trx'),
    path('view_transfer_trx', views.TransferTransactionList.as_view(), name='view_transfer_trx'),
    path('create_transfer_trx', views.create_transfer_trx, name='create_transfer_trx')
]
