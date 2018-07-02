from django import forms

class CustomDateInput(forms.DateInput):
    input_type = 'date'


class EmailForm(forms.Form):
    gmail_email = forms.EmailField(max_length=60)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())
    emails_since = forms.DateField(widget=CustomDateInput())
