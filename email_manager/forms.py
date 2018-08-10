from django import forms


class CustomDateInput(forms.DateInput):
    input_type = 'date'


class ApiEmailForm(forms.Form):
    gmail_email = forms.EmailField(max_length=60)
    emails_since = forms.DateField(widget=CustomDateInput())


class EmailForm(ApiEmailForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    field_order = ['gmail_email', 'password', 'emails_since']
