from django import forms
from . import models

class CreateClient(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = ['fname',
                  'lname',
                  'addr',
                  'acct_num',
                  'mobile_num',
                  'email_addr']

class CreateDepositTrx(forms.ModelForm):
    class Meta:
        model = models.DepositTransaction
        fields = ['trx_ref',
                  'status',
                  'client',
                  'deposit_amt',
                  'curr',
                  'current_balance',
                  'total_balance']

class CreateWithdrawTrx(forms.ModelForm):
    class Meta:
        model = models.WithdrawTransaction
        fields = ['trx_ref',
                  'status',
                  'client',
                  'withdraw_amt',
                  'curr',
                  'current_balance',
                  'total_balance']
