from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from . import forms, models

LoginRequiredMixin.login_url = "/bank/login"


class UserList(LoginRequiredMixin, ListView):
    model = User
    template_name = 'bank/user_list.html'

    def get_queryset(self):
        if 'q' in self.request.GET:
            if isinstance(self.request.GET['q'], int):
                return User.objects.filter(pk=self.request.GET['q'])
        else:
            return User.objects.all()


# todo if form is invalid show validation errors
class UserCreate(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'bank/user_create.html'
    success_url = 'user_list'
    extra_context = {'hidden': 'True'}


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserCreationForm
    template_name = 'bank/user_update.html'
    success_url = 'user_list'

    def get_context_data(self, **kwargs):
        form = UserCreationForm(instance=self.object)
        context = {'form': form, 'id': self.object.id}
        return context


class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'bank/user_delete.html'
    success_url = reverse_lazy('bank:user_list')

    def get_context_data(self, **kwargs):
        context = {'obj_client': self.object, 'id': self.object.id}
        return context


class DepositTransactionList(LoginRequiredMixin, ListView):
    model = models.DepositTransaction
    template_name = 'bank/deposit_trx_list.html'

    def get_queryset(self):
        if 'q' in self.request.GET:
            if isinstance(self.request.GET['q'], int):
                l_client = get_object_or_404(models.Client, pk=self.request.GET['q'])
                return models.DepositTransaction.objects.filter(client=l_client)
        else:
            return models.DepositTransaction.objects.all()


class DepositCreate(LoginRequiredMixin, CreateView):
    model = models.DepositTransaction
    form_class = forms.CreateDepositTrx
    template_name = 'bank/deposit_trx_create.html'
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
            return redirect('bank:deposit_trx_create')
        return response


class DepositView(LoginRequiredMixin, FormView):
    model = models.DepositTransaction
    template_name = 'bank/deposit_trx_create.html'
    success_url = 'deposit_trx_list'

    def get_context_data(self, **kwargs):
        l_id = self.kwargs['pk']
        obj_deposit_trx = get_object_or_404(models.DepositTransaction, pk=l_id)
        form = forms.CreateDepositTrx(instance=obj_deposit_trx)
        context = {'form': form,
                   'id': l_id,
                   'hidden': 'hidden',
                   'disabled': 'disabled'}
        return context


class WithdrawTransactionList(LoginRequiredMixin, ListView):
    model = models.WithdrawTransaction
    template_name = 'bank/withdraw_trx_list.html'

    def get_queryset(self):
        if 'q' in self.request.GET:
            if isinstance(self.request.GET['q'], int):
                l_client = get_object_or_404(models.Client, pk=self.request.GET['q'])
                return models.WithdrawTransaction.objects.filter(client=l_client)
        else:
            return models.WithdrawTransaction.objects.all()


class WithdrawCreate(LoginRequiredMixin, CreateView):
    model = models.WithdrawTransaction
    form_class = forms.CreateWithdrawTrx
    template_name = 'bank/withdraw_trx_create.html'
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
            return redirect('bank:withdraw_trx_create')
        return response


class WithdrawView(LoginRequiredMixin, FormView):
    model = models.WithdrawTransaction
    template_name = 'bank/withdraw_trx_create.html'
    success_url = 'withdraw_trx_list'

    def get_context_data(self, **kwargs):
        l_id = self.kwargs['pk']
        obj_withdraw_trx = get_object_or_404(models.WithdrawTransaction, pk=l_id)
        form = forms.CreateWithdrawTrx(instance=obj_withdraw_trx)
        context = {'form': form,
                   'id': l_id,
                   'hidden': 'hidden',
                   'disabled': 'disabled'}
        return context


class TransferTransactionList(LoginRequiredMixin, ListView):
    model = models.WithdrawTransaction
    template_name = 'bank/transfer_trx_list.html'

    def get_queryset(self):
        if 'q' in self.request.GET:
            if isinstance(self.request.GET['q'], int):
                l_client = get_object_or_404(models.Client, pk=self.request.GET['q'])
                return models.TransferTransaction.objects.filter(from_client=l_client)
        else:
            return models.TransferTransaction.objects.all()


class TransferCreate(LoginRequiredMixin, CreateView):
    model = models.TransferTransaction
    form_class = forms.CreateTransferTrx
    template_name = 'bank/transfer_trx_create.html'
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
            return redirect('bank:transfer_trx_create')
        return response


class TransferView(LoginRequiredMixin, FormView):
    model = models.TransferTransaction
    template_name = 'bank/transfer_trx_create.html'
    success_url = 'transfer_trx_list'

    def get_context_data(self, **kwargs):
        l_id = self.kwargs['pk']
        obj_transfer_trx = get_object_or_404(models.TransferTransaction, pk=l_id)
        form = forms.CreateTransferTrx(instance=obj_transfer_trx)
        context = {'form': form,
                   'id': l_id,
                   'hidden': 'hidden',
                   'disabled': 'disabled'}
        return context


class ClientList(LoginRequiredMixin, ListView):
    model = models.Client
    template_name = 'bank/client_list.html'

    def get_queryset(self):
        if 'q' in self.request.GET:
            if isinstance(self.request.GET['q'], int):
                return models.Client.objects.filter(pk=self.request.GET['q'])
        else:
            return models.Client.objects.all()


class ClientCreate(LoginRequiredMixin, CreateView):
    model = models.Client
    form_class = forms.ClientForm
    template_name = 'bank/client_create.html'
    success_url = 'client_list'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        if 'confirm_and_add_another' in self.request.POST:
            return redirect('bank:client_create')
        return response


class ClientUpdate(LoginRequiredMixin, UpdateView):
    model = models.Client
    form_class = forms.ClientForm
    template_name = 'bank/client_update.html'
    success_url = reverse_lazy('bank:client_list')

    def get_context_data(self, **kwargs):
        form = forms.ClientForm(instance=self.object)
        context = {'form': form, 'id': self.object.id}
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        if 'confirm_and_add_another' in self.request.POST:
            return redirect('bank:client_create')
        return response


class ClientDelete(LoginRequiredMixin, DeleteView):
    model = models.Client
    template_name = 'bank/client_delete.html'
    success_url = reverse_lazy('bank:client_list')

    def get_context_data(self, **kwargs):
        context = {'obj_client': self.object, 'id': self.object.id}
        return context


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # if user was redirected to the login page from a page inside the application
            if 'next' in request.POST:
                if request.POST['next']:
                    return redirect(request.POST.get('next'))
            return redirect('bank:about')
    else:
        form = AuthenticationForm()
    return render(request, 'bank/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('bank:login')


def about(request):
    return render(request, 'bank/about.html')


@login_required(login_url="/bank/login")
def dashboard_view(request):
    l_deposit_aggregate, l_withdraw_aggregate, l_transfer_aggregate = 0, 0, 0
    l_deposit_trx_count, l_withdraw_trx_count, l_transfer_trx_count = 0, 0, 0
    obj_list_deposit_trx = models.DepositTransaction.objects.all()
    obj_list_withdraw_trx = models.WithdrawTransaction.objects.all()
    obj_list_transfer_trx = models.TransferTransaction.objects.all()
    for item in obj_list_deposit_trx:
        l_deposit_trx_count += 1
        l_deposit_aggregate += item.deposit_amt
    for item in obj_list_withdraw_trx:
        l_withdraw_trx_count += 1
        l_withdraw_aggregate += item.withdraw_amt
    for item in obj_list_transfer_trx:
        l_transfer_trx_count += 1
        l_transfer_aggregate += item.transfer_amt
    l_trx_count = l_deposit_trx_count + l_withdraw_trx_count + l_transfer_trx_count
    l_context = {'l_deposit_aggregate': f'{l_deposit_aggregate:,}',
                 'l_withdraw_aggregate': f'{l_withdraw_aggregate:,}',
                 'l_transfer_aggregate': f'{l_transfer_aggregate:,}',
                 'l_trx_count': l_trx_count,}
    return render(request, 'bank/dashboard.html', l_context)
