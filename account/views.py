from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUp(CreateView):
    model = User
    success_url = reverse_lazy('login')
    template_name = 'account/signup.html'
    fields = ['username', 'first_name', 'last_name', 'email', 'password']
