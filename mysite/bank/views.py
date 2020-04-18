from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from . import forms, models


@login_required(login_url="/accounts/login")
def application_list(request):
    return render(request, 'bank/application_list.html')


@login_required(login_url="/accounts/login")
def client_accounts(request):
    return render(request, 'bank/client_accounts.html')


@login_required(login_url="/accounts/login")
def create_client(request):
    if request.method == 'POST':
        form = forms.CreateClient(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by, instance.balance = request.user, 0
            instance.save()
            return redirect('bank:client_accounts')
    else:
        form = forms.CreateClient()
    return render(request, 'bank/create_client.html', {'form': form})


@login_required(login_url="/accounts/login")
def edit_client(request):
    if request.method == 'POST':
        client_id = request.POST['client_id']
        selected_client = get_object_or_404(models.Client, pk=client_id)
        # Scenario: edit client form already populated and save button clicked
        if 'save_button' in request.POST:
            form = forms.CreateClient(request.POST, instance=selected_client)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.created_by = request.user
                instance.save()
                return redirect('bank:client_accounts')
        # Scenario: client ID entered and search button clicked
        else:
            form = forms.CreateClient(instance=selected_client)
            return render(request, 'bank/edit_client.html', {'form': form,
                                                             'client_id': client_id,
                                                             'readonly': 'readonly'})
    else:
        # Initial landing page of edit client
        return render(request, 'bank/edit_client.html', {'hidden': 'hidden'})


@login_required(login_url="/accounts/login")
def delete_client(request):
    if request.method == 'POST':
        client_id = request.POST['client_id']
        selected_client = get_object_or_404(models.Client, pk=client_id)
        # Scenario: delete button clicked
        if 'delete_button' in request.POST:
            selected_client.delete()
            return redirect('bank:client_accounts')
        # Scenario: client ID entered and search button clicked
        else:
            form = forms.CreateClient(instance=selected_client)
            return render(request, 'bank/delete_client.html', {'form': form,
                                                               'client_id': client_id,
                                                               'readonly': 'readonly'})
    else:
        # Initial landing page of delete client
        return render(request, 'bank/delete_client.html', {'hidden': 'hidden'})


@login_required(login_url="/accounts/login")
def create_deposit_trx(request):
    if request.method == 'POST':
        client_id = request.POST['client_id']
        selected_client = get_object_or_404(models.Client, pk=client_id)
        client_info = forms.CreateClient(instance=selected_client)
        # upon click of deposit button
        if 'deposit_button' in request.POST:
            form = forms.CreateDepositTrx(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.client = selected_client
                instance.created_by = request.user
                instance.save()
                # update balance of client
                selected_client.balance = instance.total_balance
                selected_client.save()
                return redirect('bank:application_list')
        elif 'calculate_button' in request.POST:
            form = forms.CreateDepositTrx(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.total_balance = form.cleaned_data['current_balance'] + form.cleaned_data['deposit_amt']
                form = forms.CreateDepositTrx(instance=instance)
                return render(request, 'bank/deposit_trx.html', {'form': form,
                                                                 'client_id': client_id,
                                                                 'client_info': client_info,
                                                                 'readonly': 'readonly'})

        # Scenario: client ID entered and search button clicked
        else:
            form = forms.CreateDepositTrx(initial={'current_balance': selected_client.balance})
            return render(request, 'bank/deposit_trx.html', {'form': form,
                                                             'client_id': client_id,
                                                             'client_info': client_info,
                                                             'readonly': 'readonly'})
    else:
        # Initial landing page of edit client
        return render(request, 'bank/deposit_trx.html', {'hidden': 'hidden'})


@login_required(login_url="/accounts/login")
def create_withdraw_trx(request):
    if request.method == 'POST':
        client_id = request.POST['client_id']
        selected_client = get_object_or_404(models.Client, pk=client_id)
        client_info = forms.CreateClient(instance=selected_client)
        # upon click of deposit button
        if 'deposit_button' in request.POST:
            form = forms.CreateWithdrawTrx(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.client = selected_client
                instance.created_by = request.user
                instance.save()
                # update balance of client
                selected_client.balance = instance.total_balance
                selected_client.save()
                return redirect('bank:application_list')
        elif 'calculate_button' in request.POST:
            form = forms.CreateWithdrawTrx(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.total_balance = form.cleaned_data['current_balance'] - form.cleaned_data['withdraw_amt']
                form = forms.CreateWithdrawTrx(instance=instance)
                return render(request, 'bank/withdraw_trx.html', {'form': form,
                                                                  'client_id': client_id,
                                                                  'client_info': client_info,
                                                                  'readonly': 'readonly'})

        # Scenario: client ID entered and search button clicked
        else:
            form = forms.CreateWithdrawTrx(initial={'current_balance': selected_client.balance})
            return render(request, 'bank/withdraw_trx.html', {'form': form,
                                                              'client_id': client_id,
                                                              'client_info': client_info,
                                                              'readonly': 'readonly'})
    else:
        # Initial landing page of edit client
        return render(request, 'bank/withdraw_trx.html', {'hidden': 'hidden'})


def create_transfer_trx(request):
    if request.method == 'POST':
        # info about from-client
        from_client_id = request.POST['from_client_id']
        from_client = get_object_or_404(models.Client, pk=from_client_id)
        from_client_form = forms.CreateClient(instance=from_client)
        # info about to-client
        to_client_id = request.POST['to_client_id']
        to_client = get_object_or_404(models.Client, pk=to_client_id)
        to_client_form = forms.CreateClient(instance=to_client)
        if 'search_button' in request.POST:
            # transfer form
            form = forms.CreateTransferTrx()
            return render(request, 'bank/transfer_trx.html', {'form': form,
                                                              'from_client_form': from_client_form,
                                                              'from_client_id': from_client_id,
                                                              'from_client_old_bal': from_client.balance,
                                                              'to_client_form': to_client_form,
                                                              'to_client_id': to_client_id,
                                                              'to_client_old_bal': to_client.balance,
                                                              'readonly': 'readonly'})
        elif 'calculate_button' in request.POST:
            form = forms.CreateTransferTrx(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                # todo: computation already done here. should not do computation anymore at (A)
                from_client_new_bal = from_client.balance - instance.transfer_amt
                to_client_new_bal = to_client.balance + instance.transfer_amt
                form = forms.CreateTransferTrx(instance=instance)
                return render(request, 'bank/transfer_trx.html', {'form': form,
                                                                  'from_client_form': from_client_form,
                                                                  'from_client_id': from_client_id,
                                                                  'from_client_old_bal': from_client.balance,
                                                                  'from_client_new_bal': from_client_new_bal,
                                                                  'to_client_form': to_client_form,
                                                                  'to_client_id': to_client_id,
                                                                  'to_client_old_bal': to_client.balance,
                                                                  'to_client_new_bal': to_client_new_bal,
                                                                  'readonly': 'readonly'})
        elif 'confirm_button' in request.POST:
            form = forms.CreateTransferTrx(request.POST)
            if form.is_valid():
                # transfer trx
                instance = form.save(commit=False)
                instance.from_client = from_client
                instance.to_client = to_client
                instance.created_by = request.user
                instance.save()
                # update balance from-client
                # todo: (A)
                from_client.balance = from_client.balance - instance.transfer_amt
                from_client.save()
                # update balance to-client
                to_client.balance = to_client.balance + instance.transfer_amt
                to_client.save()
                form = forms.CreateTransferTrx(instance=instance)
                return render(request, 'bank/application_list.html')
        else:
            return render(request, 'bank/transfer_trx.html')
    else:
        return render(request, 'bank/transfer_trx.html')

