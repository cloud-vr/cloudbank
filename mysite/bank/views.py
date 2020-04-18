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
            instance.created_by = request.user
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
        form = forms.CreateDepositTrx(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()
            return redirect('bank:application_list')
    else:
        form = forms.CreateDepositTrx()
    return render(request, 'bank/create_deposit_trx.html', {'form': form})


@login_required(login_url="/accounts/login")
def create_withdraw_trx(request):
    if request.method == 'POST':
        form = forms.CreateWithdrawTrx(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()
            return redirect('bank:application_list')
    else:
        form = forms.CreateWithdrawTrx()
    return render(request, 'bank/create_withdraw_trx.html', {'form': form})
