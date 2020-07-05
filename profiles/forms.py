from string import Template

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Row, HTML
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from base.forms.forms import ReadOnlyFormMixin
from profiles.models import Profile


class PictureWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = Template("""<img class="img_fill" src="$media$link"/>""")
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

    def __init__(self, *args, **kwargs):
        super(UserProfileReadOnlyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Row(
                Div(
                    Div(
                        Div(
                            HTML(
                                """
                                {% if form.image.value %}
                                    <img class="img_fill" src="{{ form.image.value.url }}">
                                {% endif %}
                                """,
                            ),
                            css_class='my-2 mx-2'
                        ),
                        css_class='d-flex border border-rounded border-secondary'
                    ),
                    css_class='col-6'
                ),
                Div(
                    'first_name',
                    'last_name',
                    'email',
                    'bio',
                    'location',
                    css_class='col-6'
                ),
                css_class='col-10 mx-auto mt-2'
            )
        )
