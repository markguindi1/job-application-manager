from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'


class EmailForm(forms.Form):
    email = forms.CharField(max_length=60)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    emails_since = forms.DateField(widget=DateInput())
