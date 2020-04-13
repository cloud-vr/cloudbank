import random

from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    fname = models.CharField('First Name', max_length=20)
    lname = models.CharField('Last Name', max_length=20)
    addr = models.CharField('Address', max_length=50)
    acct_num = models.IntegerField('Account Number')
    mobile_num = models.IntegerField('Mobile Number')
    email_addr = models.EmailField('Email Address', max_length=200)
    # Foreign Key
    created_by = models.ForeignKey(User, default=None,  on_delete=models.CASCADE)

    def __str__(self):
        return self.fname

class DepositTransaction(models.Model):
    # General Transaction Information
    trx_date = models.DateField('Date', auto_now_add=True)
    trx_ref = models.CharField(
        max_length=10,
        default=str(random.randint(1000000000, 9999999999))
    )
    status = models.CharField('Status', max_length=50)
    # Foreign Key
    created_by = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    # Client Information
    client = models.ForeignKey(Client, default=None, on_delete=models.CASCADE)
    # Transaction Computation
    deposit_amt = models.FloatField('Deposit Amount')
    curr = models.CharField('Currency', max_length=20)
    current_balance = models.FloatField('Current Balance')
    total_balance = models.FloatField('Total Balance')

    def __str__(self):
        return self.trx_ref

class WithdrawTransaction(models.Model):
    # General Transaction Information
    trx_date = models.DateField('Date', auto_now_add=True)
    trx_ref = models.CharField(
        max_length=10,
        default=str(random.randint(1000000000, 9999999999))
    )
    status = models.CharField('Status', max_length=50)
    # Foreign Key
    created_by = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    # Client Information
    client = models.ForeignKey(Client, default=None, on_delete=models.CASCADE)
    # Transaction Computation
    withdraw_amt = models.FloatField('Deposit Amount')
    curr = models.CharField('Currency', max_length=20)
    current_balance = models.FloatField('Current Balance')
    total_balance = models.FloatField('Total Balance')

    def __str__(self):
        return self.trx_ref