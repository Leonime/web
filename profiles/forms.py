from django import forms

from profiles.models import Profile


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ['location', 'bio']
