from django.contrib.auth import views
from django.shortcuts import render


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
