from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from . import forms, models

LoginRequiredMixin.login_url = "/accounts/login"


class DepositTransactionList(LoginRequiredMixin, ListView):
    model = models.DepositTransaction
    template_name = 'bank/deposit_trx_list.html'

    def get_queryset(self):
        if 'q' in self.request.GET:
            l_client = get_object_or_404(models.Client, pk=self.request.GET['q'])
            return models.DepositTransaction.objects.filter(client=l_client)
        else:
            return models.DepositTransaction.objects.all()


class DepositCreate(LoginRequiredMixin, CreateView):
    model = models.DepositTransaction
    form_class = forms.CreateDepositTrx
    template_name = 'bank/deposit_trx.html'
    success_url = 'deposit_trx_list'

    def form_valid(self, form):
        obj_client = get_object_or_404(models.Client, pk=self.request.POST['client'])
        form.instance.current_balance = obj_client.balance
        form.instance.total_balance = form.instance.current_balance + int(self.request.POST['deposit_amt'])
        form.instance.status = 'DONE'
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # update balance of the client object
        obj_client.balance = form.instance.total_balance
        obj_client.save()
        if 'confirm_and_add_another' in self.request.POST:
            return redirect('bank:create_deposit_trx')
        return response


class WithdrawTransactionList(LoginRequiredMixin, ListView):
    model = models.WithdrawTransaction
    template_name = 'bank/withdraw_trx_list.html'

    def get_queryset(self):
        if 'q' in self.request.GET:
            l_client = get_object_or_404(models.Client, pk=self.request.GET['q'])
            return models.WithdrawTransaction.objects.filter(client=l_client)
        else:
            return models.WithdrawTransaction.objects.all()


class WithdrawCreate(LoginRequiredMixin, CreateView):
    model = models.WithdrawTransaction
    form_class = forms.CreateWithdrawTrx
    template_name = 'bank/withdraw_trx.html'
    success_url = 'withdraw_trx_list'

    def form_valid(self, form):
        obj_client = get_object_or_404(models.Client, pk=self.request.POST['client'])
        form.instance.current_balance = obj_client.balance
        form.instance.total_balance = form.instance.current_balance - int(self.request.POST['withdraw_amt'])
        form.instance.status = 'DONE'
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # update balance of the client object
        obj_client.balance = form.instance.total_balance
        obj_client.save()
        if 'confirm_and_add_another' in self.request.POST:
            return redirect('bank:create_withdraw_trx')
        return response


class TransferTransactionList(LoginRequiredMixin, ListView):
    model = models.WithdrawTransaction
    template_name = 'bank/transfer_trx_list.html'

    def get_queryset(self):
        if 'q' in self.request.GET:
            l_client = get_object_or_404(models.Client, pk=self.request.GET['q'])
            return models.TransferTransaction.objects.filter(from_client=l_client)
        else:
            return models.TransferTransaction.objects.all()


class TransferCreate(LoginRequiredMixin, CreateView):
    model = models.TransferTransaction
    form_class = forms.CreateTransferTrx
    template_name = 'bank/transfer_trx.html'
    success_url = 'transfer_trx_list'

    def form_valid(self, form):
        obj_from_client = get_object_or_404(models.Client, pk=self.request.POST['from_client'])
        obj_to_client = get_object_or_404(models.Client, pk=self.request.POST['to_client'])
        form.instance.status = 'DONE'
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # update balance of the from-client object
        obj_from_client.balance = obj_from_client.balance - form.instance.transfer_amt
        obj_from_client.save()
        # update balance of the to-client object
        obj_to_client.balance = obj_to_client.balance + form.instance.transfer_amt
        obj_to_client.save()
        if 'confirm_and_add_another' in self.request.POST:
            return redirect('bank:create_transfer_trx')
        return response


class ClientList(LoginRequiredMixin, ListView):
    model = models.Client
    template_name = 'bank/client_list.html'

    def get_queryset(self):
        if 'q' in self.request.GET:
            return models.Client.objects.filter(pk=self.request.GET['q'])
        else:
            return models.Client.objects.all()


class ClientCreate(LoginRequiredMixin, CreateView):
    model = models.Client
    form_class = forms.ClientForm
    template_name = 'bank/create_client.html'
    success_url = 'client_list'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        if 'save_and_add_another' in self.request.POST:
            return redirect('bank:create_client')
        return response


class ClientUpdate(LoginRequiredMixin, UpdateView):
    model = models.Client
    form_class = forms.ClientForm
    template_name = 'bank/update_client.html'
    success_url = 'http://127.0.0.1:8000/bank/client_list'

    def get_context_data(self, **kwargs):
        obj_client = get_object_or_404(models.Client, id=self.kwargs['pk'])
        form = forms.ClientForm(instance=obj_client)
        context = {'form': form}
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        if 'save_and_add_another' in self.request.POST:
            return redirect('bank:create_client')
        return response


@login_required(login_url="/accounts/login")
def application_list(request):
    return render(request, 'bank/application_list.html')
