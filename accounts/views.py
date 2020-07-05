from django.contrib import messages
from django.contrib.auth import views, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from accounts.forms import UserCreateForm

ACCOUNT_TEMPLATES = {
    'auth': 'account/auth.html'
}


class UserLoginView(views.LoginView):
    template_name = ACCOUNT_TEMPLATES['auth']

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
    success_url = reverse_lazy('profiles:edit_profile')

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
