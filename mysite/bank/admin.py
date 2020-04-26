from django.contrib import admin

from .models import Client, DepositTransaction, WithdrawTransaction, TransferTransaction


class DepositTransactionAdmin(admin.ModelAdmin):
    list_filter = ['trx_date']


admin.site.register(Client)
admin.site.register(DepositTransaction, DepositTransactionAdmin)
admin.site.register(WithdrawTransaction)
admin.site.register(TransferTransaction)
