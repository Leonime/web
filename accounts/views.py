from django.contrib import messages
from django.contrib.auth import views, login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from accounts.forms import UserCreateForm

ACCOUNT_TEMPLATES = {
    'auth': 'account/auth.html'
}


class UserLoginView(views.LoginView):
    template_name = ACCOUNT_TEMPLATES['auth']

    def post(self, request, *args, **kwargs):
        super(UserLoginView, self).post(request, *args, **kwargs)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect(reverse('index'))
        
        context = {
            'form': self.form_class,
            'btn_label': 'Login',
        }
        messages.error(request, 'Wrong username or password, please try again.')
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        super(UserLoginView, self).get(request, *args, **kwargs)
        form = self.form_class(initial=self.initial)
        context = {
            'form': form,
            'btn_label': 'Login',
        }
        return render(request, self.template_name, context)


class UserLogoutView(views.LogoutView):
    template_name = ACCOUNT_TEMPLATES['auth']


class RegisterUserView(views.FormView):
    template_name = ACCOUNT_TEMPLATES['auth']
    form_class = UserCreateForm
    success_url = reverse_lazy('profiles:edit_profile')\
        if not getattr(settings, 'ASK_CONFIRMATION_EMAIL', False)\
        else reverse_lazy('accounts:login')

    def post(self, request, *args, **kwargs):
        super(RegisterUserView, self).get(request, *args, **kwargs)
        form = self.form_class(request.POST or None)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "User created successfully, you're now logged in.")
            return redirect(self.success_url)

        context = {
            "form": form,
            "btn_label": "Register",
        }
        return render(request, self.template_name, context)
