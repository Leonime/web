from django.contrib.auth import views, login
from django.shortcuts import render, redirect

from accounts.forms import UserCreateForm


class UserLoginView(views.LoginView):
    template_name = 'account/auth.html'

    def get(self, request, *args, **kwargs):
        super(UserLoginView, self).get(request, *args, **kwargs)
        form = self.form_class(initial=self.initial)
        context = {
            'form': form,
            'btn_label': 'Login',
        }
        return render(request, self.template_name, context)


class UserLogoutView(views.LogoutView):
    template_name = 'account/auth.html'


class RegisterUserView(views.FormView):
    template_name = 'account/auth.html'
    form_class = UserCreateForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        super(RegisterUserView, self).get(request, *args, **kwargs)
        form = self.form_class(request.POST or None)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(self.success_url)

        context = {
            "form": form,
            "btn_label": "Register",
        }
        return render(request, self.template_name, context)
