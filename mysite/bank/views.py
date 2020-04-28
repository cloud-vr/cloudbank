from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView

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


@login_required(login_url="/accounts/login")
def application_list(request):
    return render(request, 'bank/application_list.html')


@login_required(login_url="/accounts/login")
def client_accounts(request):
    return render(request, 'bank/client_accounts.html')


@login_required(login_url="/accounts/login")
def view_client(request):
    l_context = {}
    l_template = 'bank/view_client.html'
    # l_redirect = ''
    if request.method == 'POST':
        # if search button clicked
        if 'client_id' in request.POST:
            # checks if client id is populated
            if request.POST['client_id']:
                if 'search_button' in request.POST:
                    # id of the searched client
                    l_client_id = request.POST['client_id']
                    obj_searched_client = get_object_or_404(models.Client, pk=l_client_id)
                    f_create_client = forms.CreateClient(instance=obj_searched_client)
                    l_context = {'form': f_create_client,
                                 'client_id': l_client_id,
                                 'readonly': 'readonly'}  # sets the client id input box to readonly
    else:
        # GET METHOD
        l_context = l_context
    return render(request, l_template, l_context)


@login_required(login_url="/accounts/login")
def create_client(request):
    l_context = {}
    l_template = 'bank/create_client.html'
    l_redirect = 'bank:client_accounts'
    if request.method == 'POST':
        f_create_client = forms.CreateClient(request.POST)
        if f_create_client.is_valid():
            ft_create_client_ = f_create_client.save(commit=False)
            ft_create_client_.created_by = request.user
            ft_create_client_.save()
            return redirect(l_redirect)
    else:
        # GET METHOD
        f_create_client = forms.CreateClient(initial={'created_by': request.user,
                                                      'balance': 0})
        l_context = {'form': f_create_client}
    return render(request, l_template, l_context)


@login_required(login_url="/accounts/login")
def edit_client(request):
    l_context = {'hidden': 'hidden'}
    l_template = 'bank/edit_client.html'
    l_redirect = 'bank:client_accounts'
    if request.method == 'POST':
        # if search button clicked
        if 'client_id' in request.POST:
            # checks if client id is populated
            if request.POST['client_id']:
                l_client_id = request.POST['client_id']
                obj_searched_client = get_object_or_404(models.Client, pk=l_client_id)
                # if search button is clicked, return the client form with the details of the searched client
                if 'search_button' in request.POST:
                    f_create_client = forms.CreateClient(instance=obj_searched_client)
                    l_context = {'form': f_create_client,
                                 'client_id': l_client_id,
                                 'readonly': 'readonly'}
                elif 'save_button' in request.POST:
                    f_create_client = forms.CreateClient(request.POST, instance=obj_searched_client)
                    if f_create_client.is_valid():
                        ft_create_client = f_create_client.save(commit=False)
                        ft_create_client.created_by = request.user
                        ft_create_client.save()
                        return redirect(l_redirect)
    else:
        # GET METHOD
        l_context = l_context
    return render(request, l_template, l_context)


@login_required(login_url="/accounts/login")
def delete_client(request):
    l_context = {'hidden': 'hidden'}
    l_template = 'bank/delete_client.html'
    l_redirect = 'bank:client_accounts'
    if request.method == 'POST':
        # if search button clicked
        if 'client_id' in request.POST:
            # checks if client id is populated
            if request.POST['client_id']:
                l_client_id = request.POST['client_id']
                obj_searched_client = get_object_or_404(models.Client, pk=l_client_id)
                # if search button is clicked, return the client form with the details of the searched client
                if 'search_button' in request.POST:
                    f_create_client = forms.CreateClient(instance=obj_searched_client)
                    l_context = {'form': f_create_client,
                                 'client_id': l_client_id,
                                 'readonly': 'readonly'}
                # if delete button clicked
                elif 'delete_button' in request.POST:
                    obj_searched_client.delete()
                    return redirect(l_redirect)
    else:
        # GET METHOD
        l_context = l_context
    return render(request, l_template, l_context)