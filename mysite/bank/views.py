import random
from datetime import date

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from . import forms, models


class DepositTransactionList(ListView):
    model = models.DepositTransaction
    template_name = 'bank/deposit_trx_list.html'

    def get_queryset(self):
        if 'q' in self.request.GET:
            l_client = get_object_or_404(models.Client, pk=self.request.GET['q'])
            return models.DepositTransaction.objects.filter(client=l_client)
        else:
            return models.DepositTransaction.objects.all()


class WithdrawTransactionList(ListView):
    model = models.WithdrawTransaction
    template_name = 'bank/withdraw_trx_list.html'

    def get_queryset(self):
        if 'q' in self.request.GET:
            l_client = get_object_or_404(models.Client, pk=self.request.GET['q'])
            return models.WithdrawTransaction.objects.filter(client=l_client)
        else:
            return models.WithdrawTransaction.objects.all()


class TransferTransactionList(ListView):
    model = models.WithdrawTransaction
    template_name = 'bank/transfer_trx_list.html'

    def get_queryset(self):
        if 'q' in self.request.GET:
            l_client = get_object_or_404(models.Client, pk=self.request.GET['q'])
            return models.TransferTransaction.objects.filter(from_client=l_client)
        else:
            return models.TransferTransaction.objects.all()


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


@login_required(login_url="/accounts/login")
def create_deposit_trx(request):
    l_context = {'hidden': 'hidden'}
    l_template = 'bank/deposit_trx.html'
    l_redirect = 'bank:view_deposit_trx'
    if request.method == 'POST':
        # if search button clicked
        if 'client_id' in request.POST:
            # checks if client id is populated
            if request.POST['client_id']:
                l_client_id = request.POST['client_id']
                obj_searched_client = get_object_or_404(models.Client, pk=l_client_id)
                f_create_client = forms.CreateClient(instance=obj_searched_client)
                # upon click of search button
                if 'search_button' in request.POST:
                    l_balance = obj_searched_client.balance
                    l_ref = str(random.randint(1000000000, 9999999999))
                    f_create_deposit_trx = forms.CreateDepositTrx(
                        initial={'trx_date': date.today(),
                                 'trx_ref': l_ref,
                                 'status': 'Open',
                                 'current_balance': l_balance,
                                 'total_balance': l_balance})
                    l_context = {'form': f_create_deposit_trx,
                                 'client_id': l_client_id,
                                 'client_info': f_create_client,
                                 'readonly': 'readonly'}
                # upon click of calculate button
                elif 'calculate_button' in request.POST:
                    f_create_deposit_trx = forms.CreateDepositTrx(request.POST)
                    if f_create_deposit_trx.is_valid():
                        ft_create_deposit_trx = f_create_deposit_trx.save(commit=False)
                        ft_create_deposit_trx.total_balance = f_create_deposit_trx.cleaned_data['current_balance'] + \
                                                              f_create_deposit_trx.cleaned_data['deposit_amt']
                        f_create_deposit_trx = forms.CreateDepositTrx(instance=ft_create_deposit_trx)
                        l_context = {'form': f_create_deposit_trx,
                                     'client_id': l_client_id,
                                     'client_info': f_create_client,
                                     'readonly': 'readonly'}
                # upon click of deposit button
                elif 'deposit_button' in request.POST:
                    f_create_deposit_trx = forms.CreateDepositTrx(request.POST)
                    if f_create_deposit_trx.is_valid():
                        ft_create_deposit_trx = f_create_deposit_trx.save(commit=False)
                        ft_create_deposit_trx.client = obj_searched_client
                        ft_create_deposit_trx.created_by = request.user
                        l_total_balance = f_create_deposit_trx.cleaned_data['current_balance'] + \
                                          f_create_deposit_trx.cleaned_data['deposit_amt']
                        ft_create_deposit_trx.total_balance = l_total_balance
                        ft_create_deposit_trx.status = 'Done'
                        ft_create_deposit_trx.save()
                        # update balance of the client object
                        obj_searched_client.balance = l_total_balance
                        obj_searched_client.save()
                        return redirect(l_redirect)
    else:
        # GET METHOD: Initial landing page of edit client
        l_context = l_context
    return render(request, l_template, l_context)


@login_required(login_url="/accounts/login")
def create_withdraw_trx(request):
    l_context = {'hidden': 'hidden'}
    l_template = 'bank/withdraw_trx.html'
    l_redirect = 'bank:view_withdraw_trx'
    if request.method == 'POST':
        # if search button clicked
        if 'client_id' in request.POST:
            # checks if client id is populated
            if request.POST['client_id']:
                l_client_id = request.POST['client_id']
                obj_searched_client = get_object_or_404(models.Client, pk=l_client_id)
                f_create_client = forms.CreateClient(instance=obj_searched_client)
                if 'search_button' in request.POST:
                    l_balance = obj_searched_client.balance
                    l_ref = str(random.randint(1000000000, 9999999999))
                    f_create_withdraw_trx = forms.CreateWithdrawTrx(
                        initial={'trx_date': date.today(),
                                 'trx_ref': l_ref,
                                 'status': 'Open',
                                 'current_balance': obj_searched_client.balance,
                                 'total_balance': l_balance})
                    l_context = {'form': f_create_withdraw_trx,
                                 'client_id': l_client_id,
                                 'client_info': f_create_client,
                                 'readonly': 'readonly'}
                elif 'calculate_button' in request.POST:
                    f_create_withdraw_trx = forms.CreateWithdrawTrx(request.POST)
                    if f_create_withdraw_trx.is_valid():
                        ft_create_withdraw_trx = f_create_withdraw_trx.save(commit=False)
                        ft_create_withdraw_trx.total_balance = f_create_withdraw_trx.cleaned_data['current_balance'] - \
                                                               f_create_withdraw_trx.cleaned_data['withdraw_amt']
                        f_create_withdraw_trx = forms.CreateWithdrawTrx(instance=ft_create_withdraw_trx)
                        l_context = {'form': f_create_withdraw_trx,
                                     'client_id': l_client_id,
                                     'client_info': f_create_client,
                                     'readonly': 'readonly'}
                # upon click of deposit button
                elif 'withdraw_button' in request.POST:
                    f_create_withdraw_trx = forms.CreateWithdrawTrx(request.POST)
                    if f_create_withdraw_trx.is_valid():
                        ft_create_withdraw_trx = f_create_withdraw_trx.save(commit=False)
                        ft_create_withdraw_trx.client = obj_searched_client
                        ft_create_withdraw_trx.created_by = request.user
                        l_total_balance = f_create_withdraw_trx.cleaned_data['current_balance'] - \
                                          f_create_withdraw_trx.cleaned_data['withdraw_amt']
                        ft_create_withdraw_trx.total_balance = l_total_balance
                        ft_create_withdraw_trx.status = 'Done'
                        ft_create_withdraw_trx.save()
                        # update balance of client
                        obj_searched_client.balance = l_total_balance
                        obj_searched_client.save()
                        return redirect(l_redirect)
    else:
        # GET METHOD: Initial landing page of edit client
        l_context = l_context
    return render(request, l_template, l_context)


def create_transfer_trx(request):
    l_context = {}
    l_template = 'bank/transfer_trx.html'
    l_redirect = 'bank:view_transfer_trx'
    if request.method == 'POST':
        # if search button clicked
        if 'from_client_id' in request.POST and 'to_client_id' in request.POST:
            # checks if client id is populated
            if request.POST['from_client_id'] and request.POST['to_client_id']:
                # info about from-client
                l_from_client_id = request.POST['from_client_id']
                obj_from_client = get_object_or_404(models.Client, pk=l_from_client_id)
                f_from_client = forms.CreateClient(instance=obj_from_client)
                # info about to-client
                l_to_client_id = request.POST['to_client_id']
                obj_to_client = get_object_or_404(models.Client, pk=l_to_client_id)
                f_to_client = forms.CreateClient(instance=obj_to_client)
                if 'search_button' in request.POST:
                    l_ref = str(random.randint(1000000000, 9999999999))
                    f_create_transfer_trx = forms.CreateTransferTrx(initial={'trx_date': date.today(),
                                                                             'trx_ref': l_ref,
                                                                             'status': 'Open'})
                    l_context = {'form': f_create_transfer_trx,
                                 'from_client_form': f_from_client,
                                 'from_client_id': l_from_client_id,
                                 'from_client_old_bal': obj_from_client.balance,
                                 'to_client_form': f_to_client,
                                 'to_client_id': l_to_client_id,
                                 'to_client_old_bal': obj_to_client.balance,
                                 'readonly': 'readonly'}
                elif 'calculate_button' in request.POST:
                    f_create_transfer_trx = forms.CreateTransferTrx(request.POST)
                    if f_create_transfer_trx.is_valid():
                        ft_create_transfer_trx = f_create_transfer_trx.save(commit=False)
                        l_from_client_new_bal = obj_from_client.balance - ft_create_transfer_trx.transfer_amt
                        l_to_client_new_bal = obj_to_client.balance + ft_create_transfer_trx.transfer_amt
                        f_create_transfer_trx = forms.CreateTransferTrx(instance=ft_create_transfer_trx)
                        l_context = {'form': f_create_transfer_trx,
                                     'from_client_form': f_from_client,
                                     'from_client_id': l_from_client_id,
                                     'from_client_old_bal': obj_from_client.balance,
                                     'from_client_new_bal': l_from_client_new_bal,
                                     'to_client_form': f_to_client,
                                     'to_client_id': l_to_client_id,
                                     'to_client_old_bal': obj_to_client.balance,
                                     'to_client_new_bal': l_to_client_new_bal,
                                     'readonly': 'readonly'}
                elif 'confirm_button' in request.POST:
                    f_create_transfer_trx = forms.CreateTransferTrx(request.POST)
                    if f_create_transfer_trx.is_valid():
                        # transfer trx
                        ft_create_transfer_trx = f_create_transfer_trx.save(commit=False)
                        ft_create_transfer_trx.from_client = obj_from_client
                        ft_create_transfer_trx.to_client = obj_to_client
                        ft_create_transfer_trx.created_by = request.user
                        ft_create_transfer_trx.status = 'Done'
                        ft_create_transfer_trx.save()
                        # update balance from-client
                        obj_from_client.balance = obj_from_client.balance - ft_create_transfer_trx.transfer_amt
                        obj_from_client.save()
                        # update balance to-client
                        obj_to_client.balance = obj_to_client.balance + ft_create_transfer_trx.transfer_amt
                        obj_to_client.save()
                        return redirect(l_redirect)
    else:
        # GET METHOD: initial landing page of view deposit transactions
        l_context = {}
    return render(request, l_template, l_context)
