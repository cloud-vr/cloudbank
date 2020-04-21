from gc import disable

from django import forms
from django.forms import ModelForm

from . import models


class CreateClient(ModelForm):
    class Meta:
        model = models.Client
        fields = ['fname',
                  'lname',
                  'addr',
                  'acct_num',
                  'mobile_num',
                  'email_addr']


class CreateDepositTrx(ModelForm):
    total_balance = forms.FloatField(disabled=True)
    current_balance = forms.FloatField(disabled=True)
    # curr = forms.FloatField(disabled=True)

    class Meta:
        model = models.DepositTransaction
        fields = ['trx_ref',
                  'status',
                  'deposit_amt',
                  'curr',
                  'current_balance',
                  'total_balance']


class CreateWithdrawTrx(ModelForm):
    total_balance = forms.FloatField(required=False)

    class Meta:
        model = models.WithdrawTransaction
        fields = ['trx_ref',
                  'status',
                  'withdraw_amt',
                  'curr',
                  'current_balance',
                  'total_balance']


class CreateTransferTrx(ModelForm):
    class Meta:
        model = models.TransferTransaction
        fields = ['trx_ref',
                  'status',
                  'transfer_amt',
                  'curr']
