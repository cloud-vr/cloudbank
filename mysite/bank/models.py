import random

from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    fname = models.CharField('First Name', max_length=20)
    lname = models.CharField('Last Name', max_length=20)
    addr = models.CharField('Address', max_length=50)
    acct_num = models.IntegerField('Account Number')
    mobile_num = models.IntegerField('Mobile Number')
    email_addr = models.EmailField('Email Address', max_length=200)
    balance = models.FloatField('Account Balance')
    # Foreign Key
    created_by = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.fname


class DepositTransaction(models.Model):
    # General Transaction Information
    trx_date = models.DateField('Date')
    trx_ref = models.CharField('Reference #', max_length=10)
    status = models.CharField('Status', max_length=50)
    # Foreign Key
    created_by = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    # Client Information
    client = models.ForeignKey(Client, default=None, on_delete=models.CASCADE)
    # Transaction Computation
    deposit_amt = models.FloatField('Deposit Amount')
    curr = models.CharField('Currency', default='PHP', max_length=20)
    current_balance = models.FloatField('Current Balance')
    total_balance = models.FloatField('Total Balance')

    def __str__(self):
        return self.trx_ref


class WithdrawTransaction(models.Model):
    # General Transaction Information
    trx_date = models.DateField('Date')
    trx_ref = models.CharField('Reference #', max_length=10)
    status = models.CharField('Status', max_length=50)
    # Foreign Key
    created_by = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    # Client Information
    client = models.ForeignKey(Client, default=None, on_delete=models.CASCADE)
    # Transaction Computation
    withdraw_amt = models.FloatField('Withdraw Amount')
    curr = models.CharField('Currency', default='PHP', max_length=20)
    current_balance = models.FloatField('Current Balance')
    total_balance = models.FloatField('Total Balance')

    def __str__(self):
        return self.trx_ref


class TransferTransaction(models.Model):
    # General Transaction Information
    trx_date = models.DateField('Date')
    trx_ref = models.CharField('Reference #', max_length=10)
    status = models.CharField('Status', max_length=50)
    # Foreign Key
    created_by = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    # Client Information
    from_client = models.ForeignKey(Client, related_name='from_client', default=None, on_delete=models.CASCADE)
    to_client = models.ForeignKey(Client, related_name='to_client', default=None, on_delete=models.CASCADE)
    # Transaction Computation
    transfer_amt = models.FloatField('Transfer Amount')
    curr = models.CharField('Currency', default='PHP', max_length=20)

    def __str__(self):
        return self.trx_ref
