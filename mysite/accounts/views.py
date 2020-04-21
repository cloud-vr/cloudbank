from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def user_list(request):
    obj_list_user = User.objects.all()
    return render(request, 'accounts/user_list.html', {'obj_list_user': obj_list_user})


def create_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('account:user_list')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/create_user.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # if user was redirected to the login page from a page inside the application
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            # user started from the login page
            else:
                return redirect('bank:application_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')
