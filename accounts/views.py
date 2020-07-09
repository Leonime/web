import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.html import format_html
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from accounts.forms import UserCreateForm
from core.tokens import UserTokenGenerator
from core.utils import send_confirmation_email

ACCOUNT_TEMPLATES = {
    'auth': 'account/auth.html'
}
logger = logging.getLogger(__name__)


class UserLoginView(views.LoginView):
    template_name = ACCOUNT_TEMPLATES['auth']

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user: User = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.profile.email_confirmed:
                token = UserTokenGenerator().make_token(user)
                user_id = urlsafe_base64_encode(force_bytes(user.id))
                url = reverse('accounts:resend-confirm_email', kwargs={'user_id': user_id, 'token': token})
                message = format_html(f'You need to confirm your email to login. '
                                      f'<a href="{url}">Resend confirmation email.</a>')
                messages.error(request, message)
                return redirect(reverse('index'))
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
        ace: bool = getattr(settings, 'ASK_CONFIRMATION_EMAIL', False)
        form = self.form_class(request.POST or None)
        context = {
            "form": form,
            "btn_label": "Register",
        }

        if form.is_valid():
            user: User = form.save(commit=False) if ace else form.save()
            user.save()
            if ace:
                token = UserTokenGenerator().make_token(user)
                user_id = urlsafe_base64_encode(force_bytes(user.id))
                return send_confirmation_email(request, user, user_id, token, context, self.success_url)
            else:
                login(request, user)
                messages.success(request, "User created successfully, you're now logged in.")
                return redirect(self.success_url)
        return render(request, self.template_name, context)


class ConfirmRegistrationView(View):

    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))
        user = User.objects.get(pk=user_id)

        context = {
            'form': AuthenticationForm(),
        }
        if user and UserTokenGenerator().check_token(user, token):
            profile = user.profile
            profile.email_confirmed = True
            profile.save()
            messages.success(request, "Registration complete. Please login")
            return redirect(reverse('accounts:login'))
        else:
            messages.error(request, 'Registration confirmation error. '
                                    'Please click the reset password to generate a new confirmation email.')

        return render(request, ACCOUNT_TEMPLATES['auth'], context)


class ResendConfirmRegistrationView(View):

    def get(self, request, user_id, token):
        user_id = force_text(urlsafe_base64_decode(user_id))
        user = User.objects.get(pk=user_id)

        context = {
            'form': AuthenticationForm(),
        }
        if user and UserTokenGenerator().check_token(user, token):
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            return send_confirmation_email(request, user, user_id, token, context, reverse('index'), True)
        else:
            messages.error(request, 'Registration confirmation error. '
                                    'Please click the reset password to generate a new confirmation email.')

        return render(request, ACCOUNT_TEMPLATES['auth'], context)
