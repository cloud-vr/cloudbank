from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class UserList(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'

    def get_queryset(self):
        if 'q' in self.request.GET:
            return User.objects.filter(pk=self.request.GET['q'])
        else:
            return User.objects.all()

# todo if form is invalid show validation errors
class UserCreate(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/create_user.html'
    success_url = 'user_list'
    extra_context = {'hidden': 'True'}


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/update_user.html'
    success_url = 'user_list'

    def get_context_data(self, **kwargs):
        form = UserCreationForm(instance=self.object)
        context = {'form': form, 'id': self.object.id}
        return context

class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/delete_user.html'
    success_url = 'http://127.0.0.1:8000/accounts/user_list'  # TODO fix this

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
            return redirect('bank:application_list')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')
