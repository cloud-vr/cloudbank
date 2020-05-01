from django.urls import path

from . import views

app_name = 'bank'

urlpatterns = [
    # Users
    path('user_list', views.UserList.as_view(), name='user_list'),
    path('user_create', views.UserCreate.as_view(), name='user_create'),
    path('user_update/<int:pk>/', views.UserUpdate.as_view(), name='user_update'),
    path('user_delete/<int:pk>/', views.UserDelete.as_view(), name='user_delete'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    # Application List
    path('application_list', views.application_list, name='application_list'),
    # Client
    path('client_list', views.ClientList.as_view(), name='client_list'),
    path('client_create', views.ClientCreate.as_view(), name='client_create'),
    path('client_update/<int:pk>/', views.ClientUpdate.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', views.ClientDelete.as_view(), name='client_delete'),
    # Deposit
    path('deposit_trx_list', views.DepositTransactionList.as_view(), name='deposit_trx_list'),
    path('deposit_trx_view/<int:pk>/', views.DepositView.as_view(), name='deposit_trx_view'),
    path('deposit_trx_create', views.DepositCreate.as_view(), name='deposit_trx_create'),
    # Withdraw
    path('withdraw_trx_list', views.WithdrawTransactionList.as_view(), name='withdraw_trx_list'),
    path('withdraw_trx_view/<int:pk>/', views.WithdrawView.as_view(), name='withdraw_trx_view'),
    path('withdraw_trx_create', views.WithdrawCreate.as_view(), name='withdraw_trx_create'),
    # Transfer
    path('transfer_trx_list', views.TransferTransactionList.as_view(), name='transfer_trx_list'),
    path('transfer_trx_view/<int:pk>/', views.TransferView.as_view(), name='transfer_trx_view'),
    path('transfer_trx_create', views.TransferCreate.as_view(), name='transfer_trx_create')
]
