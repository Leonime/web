from string import Template

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from base.forms import ReadOnlyFormMixin
from profiles.models import Profile


class PictureWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = Template("""<img class="cover" src="$media$link" width="128" height="128"/>""")
        return mark_safe(html.substitute(media=settings.MEDIA_URL, link=value))


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.CharField(required=False)

    field_order = ['first_name', 'last_name', 'email', 'image', 'bio', 'location']

    class Meta:
        model = Profile
        fields = ['location', 'bio', 'image']


class UserProfileReadOnlyForm(ReadOnlyFormMixin):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.CharField(required=False)
    image = forms.ImageField(widget=PictureWidget, label='Profile Picture', required=False)

    field_order = ['image', 'first_name', 'last_name', 'email', 'bio', 'location']

    class Meta:
        model = Profile
        fields = ['location', 'bio', 'image']
