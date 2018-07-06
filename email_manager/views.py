from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .get_emails import *
from .forms import *
import datetime
import json
import imaplib

# Create your views here.

class EmailFormView(LoginRequiredMixin, FormView):
    template_name = "email_manager/email-form.html"
    form_class = EmailForm
    success_url = reverse_lazy('email_manager:emails-list')

    def form_valid(self, form):
        # Get email, pswd, since_date, use them to get emails
        email_address = form.cleaned_data['gmail_email']
        pswd = form.cleaned_data['password']
        date_from = form.cleaned_data['emails_since']

        # If authentication fails, redirect to email login page with prepopulated form
        # (by returning self.form_invalid(form)) and display "Invalid credentials" error message
        try:
            emails_list = get_emails(email_address, pswd, date_from)
        except imaplib.IMAP4.error as e:
            credens_error = ValidationError("Invalid credentials", code="invalid_credens")
            form.add_error(None, credens_error)
            return self.form_invalid(form)

        # Serialize emails list to JSON for adding to session dict
        emails_json = json.dumps([email.__dict__ for email in emails_list])
        self.request.session['emails'] = emails_json

        # Return Httpresponse:
        return super().form_valid(form)

class EmailsListView(LoginRequiredMixin, TemplateView):
    template_name = "email_manager/emails-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emails_json = self.request.session['emails']

        # Un-serialize JSON email list, back to Python list for use in template context
        emails_list = json.loads(emails_json)
        context['emails'] = emails_list

        return context
