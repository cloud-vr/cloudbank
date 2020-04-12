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
            # save article to db
            return redirect('bank:application_list')
    else:
        form = forms.CreateClient()
    return render(request, 'bank/create_client.html', {'form': form})