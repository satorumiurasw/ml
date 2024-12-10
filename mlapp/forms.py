from django import forms
from .models import Customer

class InputForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Customer
        exclude = ['id', 'result', 'proba', 'comment', 'registered_date']
