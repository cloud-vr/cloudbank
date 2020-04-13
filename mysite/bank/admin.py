from django.contrib import admin

from .models import Client, DepositTransaction, WithdrawTransaction

admin.site.register(Client)
admin.site.register(DepositTransaction)
admin.site.register(WithdrawTransaction)

