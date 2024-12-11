from django import forms
from .models import Customer
from django.contrib.auth.forms import AuthenticationForm

class InputForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Customer
        exclude = ['id', 'result', 'proba', 'comment', 'registered_date']

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
