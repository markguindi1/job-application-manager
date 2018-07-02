from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.core import serializers
from django.core.exceptions import ValidationError
from .models import *
from .get_emails import *
from .forms import *
import datetime
import json

# Create your views here.

class EmailFormView(FormView):
    template_name = "email_manager/email-form.html"
    form_class = EmailForm
    success_url = reverse_lazy('email_manager:emails-list')

    def form_valid(self, form):
        # Get email, pswd, since_date, use them to get emails
        email_address = form.cleaned_data['gmail_email']
        pswd = form.cleaned_data['password']
        date_from = form.cleaned_data['emails_since']

        try:
            emails_list = get_emails(email_address, pswd, date_from)
        except Exception as e:
            #credens_error = ValidationError(_("Invalid credentials"), code="invalid_credens")
            credens_error = ValidationError("Invalid credentials", code="invalid_credens")
            form.add_error(None, credens_error)
            print(form.non_field_errors())
            return self.form_invalid(form)

        # Serialize emails list to JSON for adding to session dict
        emails_json = json.dumps([email.__dict__ for email in emails_list])
        self.request.session['emails'] = emails_json

        # Return Httpresponse:
        return super().form_valid(form)

class EmailsListView(TemplateView):
    template_name = "email_manager/emails-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emails_json = self.request.session['emails']

        # Un-serialize JSON email list, back to Python list for use in template context
        emails_list = json.loads(emails_json)
        context['emails'] = emails_list

        return context
