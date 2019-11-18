from django.contrib.admin import ModelAdmin
from django.forms import ModelForm, MultipleChoiceField, CheckboxSelectMultiple

from base.models import Weekday
from testing.models import Testing


class TestingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TestingForm, self).__init__(*args, **kwargs)
        self.fields['dow'].widget = CheckboxSelectMultiple()
        self.fields['dow'].queryset = Weekday.objects.all()
        self.fields['dow'].help_text = ''

    class Meta:
        model = Testing
        fields = ['dow']

    def clean_dow(self):
        # do something that validates your data
        return self.cleaned_data['dow']


class TestingAdmin(ModelAdmin):
    form = TestingForm
