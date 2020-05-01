import random
from datetime import date

from django import forms
from django.forms import ModelForm

from . import models


class ClientForm(ModelForm):
    acct_num = forms.IntegerField(widget=forms.TextInput(attrs={'readonly': '',
                                                             'style': 'background-color:#d3d3d3;',
                                                             'value': random.randint(1000000000, 9999999999)}))
    balance = forms.FloatField(widget=forms.TextInput(attrs={'readonly': '',
                                                             'style': 'background-color:#d3d3d3;',
                                                             'value': 0}))

    class Meta:
        model = models.Client
        fields = ['fname',
                  'lname',
                  'addr',
                  'acct_num',
                  'mobile_num',
                  'email_addr',
                  'balance']


class CreateDepositTrx(ModelForm):
    trx_date = forms.CharField(widget=forms.TextInput(attrs={'readonly': '',
                                                             'style': 'background-color:#d3d3d3;',
                                                             'value': date.today()}))
    trx_ref = forms.CharField(widget=forms.TextInput(attrs={'readonly': '',
                                                            'style': 'background-color:#d3d3d3;',
                                                            'value': random.randint(1000000000, 9999999999)}))
    status = forms.CharField(widget=forms.TextInput(attrs={'readonly': '',
                                                           'style': 'background-color:#d3d3d3;',
                                                           'value': 'OPEN'}))

    class Meta:
        model = models.DepositTransaction
        fields = ['trx_date',
                  'trx_ref',
                  'status',
                  'client',
                  'deposit_amt',
                  'curr']


class CreateWithdrawTrx(ModelForm):
    trx_date = forms.CharField(widget=forms.TextInput(attrs={'readonly': '',
                                                             'style': 'background-color:#d3d3d3;',
                                                             'value': date.today()}))
    trx_ref = forms.CharField(widget=forms.TextInput(attrs={'readonly': '',
                                                            'style': 'background-color:#d3d3d3;',
                                                            'value': random.randint(1000000000, 9999999999)}))
    status = forms.CharField(widget=forms.TextInput(attrs={'readonly': '',
                                                           'style': 'background-color:#d3d3d3;',
                                                           'value': 'OPEN'}))

    class Meta:
        model = models.WithdrawTransaction
        fields = ['trx_date',
                  'trx_ref',
                  'status',
                  'client',
                  'withdraw_amt',
                  'curr']


class CreateTransferTrx(ModelForm):
    trx_date = forms.CharField(widget=forms.TextInput(attrs={'readonly': '',
                                                             'style': 'background-color:#d3d3d3;',
                                                             'value': date.today()}))
    trx_ref = forms.CharField(widget=forms.TextInput(attrs={'readonly': '',
                                                            'style': 'background-color:#d3d3d3;',
                                                            'value': random.randint(1000000000, 9999999999)}))
    status = forms.CharField(widget=forms.TextInput(attrs={'readonly': '',
                                                           'style': 'background-color:#d3d3d3;',
                                                           'value': 'OPEN'}))

    class Meta:
        model = models.TransferTransaction
        fields = ['trx_date',
                  'trx_ref',
                  'status',
                  'from_client',
                  'to_client',
                  'transfer_amt',
                  'curr']
