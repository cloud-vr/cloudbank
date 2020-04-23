from django.contrib import admin

from .models import Client, DepositTransaction, WithdrawTransaction, TransferTransaction

admin.site.register(Client)
admin.site.register(DepositTransaction)
admin.site.register(WithdrawTransaction)
admin.site.register(TransferTransaction)
