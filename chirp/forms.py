from django import forms
from django.conf import settings

from chirp.models import Chirp


class ChirpForm(forms.ModelForm):
    class Meta:
        model = Chirp
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > settings.MAX_CHIRP_LENGTH:
            raise forms.ValidationError("This chirp is too long")
        return content
