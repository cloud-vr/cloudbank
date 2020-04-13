from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms

@login_required(login_url="/accounts/login")
def application_list(request):
    return render(request, 'bank/application_list.html')

@login_required(login_url="/accounts/login")
def create_client(request):
    if request.method == 'POST':
        form = forms.CreateClient(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()
            return redirect('bank:application_list')
    else:
        form = forms.CreateClient()
    return render(request, 'bank/create_client.html', {'form': form})

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
