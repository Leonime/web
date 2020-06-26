from django.forms import ModelForm


class ReadOnlyFormMixin(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReadOnlyFormMixin, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs['readonly'] = True

    def save(self, *args, **kwargs):
        # Override save so there's no possibility of anything getting saved.
        pass
