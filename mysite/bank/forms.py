from django import forms
from django.forms import ModelForm

from . import models


class CreateClient(ModelForm):
    balance = forms.FloatField(widget=forms.TextInput(attrs={'readonly': ''}))

    class Meta:
        model = models.Client
        fields = ['fname',
                  'lname',
                  'addr',
                  'acct_num',
                  'mobile_num',
                  'email_addr',
                  'balance',
                  'created_by']


class CreateDepositTrx(ModelForm):
    trx_date = forms.CharField(widget=forms.TextInput(attrs={'readonly': ''}))
    trx_ref = forms.CharField(widget=forms.TextInput(attrs={'readonly': ''}))
    status = forms.CharField(widget=forms.TextInput(attrs={'readonly': ''}))
    current_balance = forms.FloatField(widget=forms.TextInput(attrs={'readonly': ''}))
    total_balance = forms.FloatField(widget=forms.TextInput(attrs={'readonly': ''}))

    class Meta:
        model = models.DepositTransaction
        fields = ['trx_date',
                  'trx_ref',
                  'status',
                  'deposit_amt',
                  'curr',
                  'current_balance',
                  'total_balance']


class CreateWithdrawTrx(ModelForm):
    trx_date = forms.CharField(widget=forms.TextInput(attrs={'readonly': ''}))
    trx_ref = forms.CharField(widget=forms.TextInput(attrs={'readonly': ''}))
    status = forms.CharField(widget=forms.TextInput(attrs={'readonly': ''}))
    current_balance = forms.FloatField(widget=forms.TextInput(attrs={'readonly': ''}))
    total_balance = forms.FloatField(widget=forms.TextInput(attrs={'readonly': ''}))

    class Meta:
        model = models.WithdrawTransaction
        fields = ['trx_date',
                  'trx_ref',
                  'status',
                  'withdraw_amt',
                  'curr',
                  'current_balance',
                  'total_balance']


class CreateTransferTrx(ModelForm):
    trx_date = forms.CharField(widget=forms.TextInput(attrs={'readonly': ''}))
    trx_ref = forms.CharField(widget=forms.TextInput(attrs={'readonly': ''}))
    status = forms.CharField(widget=forms.TextInput(attrs={'readonly': ''}))

    class Meta:
        model = models.TransferTransaction
        fields = ['trx_date',
                  'trx_ref',
                  'status',
                  'transfer_amt',
                  'curr']
