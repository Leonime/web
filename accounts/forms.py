from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label='eMail')
    error_messages = {
        'email_exists': 'The email already exists.'
    }

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        field_classes = {
            'email': forms.EmailField
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError(
                self.error_messages['email_exists'],
                code='email_exists',
            )
        return email

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
