from django import forms

from chirp.models import Chirp

MAX_TWEET_LENGTH = 240


class ChirpForm(forms.ModelForm):
    class Meta:
        model = Chirp
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError("This chirp is too long")
        return content
