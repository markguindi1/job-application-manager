from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .get_emails import *
from .forms import *
from .get_emails_api import *
import datetime
import json
import imaplib

# Create your views here.


class EmailAccountsListView(LoginRequiredMixin, ListView):
    model = EmailAddress
    template_name = "email_manager/email-address-list.html"
    context_object_name = 'email_addresses'

    def get_queryset(self):
        queryset = super(EmailAccountsListView, self).get_queryset().filter(user=self.request.user)
        return queryset


class EmailAccountCreate(LoginRequiredMixin, CreateView):
    model = EmailAddress
    fields = ["address"]
    template_name = "email_manager/email-address-form.html"
    success_url = reverse_lazy("email_manager:email_address_list")

    # Overridden in order to set the new application's user to the current user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EmailAccountUpdate(LoginRequiredMixin, UpdateView):
    model = EmailAddress
    fields = ["address"]
    template_name = "email_manager/email-address-form.html"
    success_url = reverse_lazy("email_manager:email_address_list")

    def get_queryset(self):
        return super(EmailAccountUpdate, self).get_queryset().filter(user=self.request.user)


class EmailAccountDelete(LoginRequiredMixin, DeleteView):
    model = EmailAddress
    fields = ["address"]
    template_name = "email_manager/email-address-delete-form.html"
    success_url = reverse_lazy("email_manager:email_address_list")

    def get_queryset(self):
        return super(EmailAccountDelete, self).get_queryset().filter(user=self.request.user)


class EmailFormView(LoginRequiredMixin, FormView):
    template_name = "email_manager/email-form.html"
    success_url = reverse_lazy('email_manager:email_list')

    def get_form_class(self):
        if self.emails_from_api:
            return ApiEmailForm
        return EmailForm

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)

        if self.email_addr is not None:
            form.initial = {"gmail_email": self.email_addr}
        context['form'] = form
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        # Check if emails can be retrieved from API or not.
        # If yes, use ApiEmailForm and get emails from API,
        # otherwise use EmailForm and get emails using plain Python libraries.
        try:
            self.email_addr = self.request.GET["email_addr"]
            self.emails_from_api = True
        except:
            self.email_addr = None
            self.emails_from_api = False

        return super(EmailFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Get email, pswd, since_date, use them to get emails
        email_address = form.cleaned_data['gmail_email']
        if not self.emails_from_api:
            pswd = form.cleaned_data['password']
        else:
            pswd = ""
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
        emails_json = json.dumps(emails_list, cls=EmailEncoder)
        self.request.session['emails'] = emails_json

        # Return Httpresponse:
        return super().form_valid(form)


class EmailsListView(LoginRequiredMixin, TemplateView):
    template_name = "email_manager/emails-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emails_json = self.request.session['emails']

        # Un-serialize JSON email list, back to Python list for use in template context
        emails_list = json.loads(emails_json, object_hook=email_decoder)
        context['emails'] = emails_list

        return context


class EmailContentView(LoginRequiredMixin, TemplateView):
    template_name = "email_manager/email-content.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emails_json = self.request.session['emails']
        #del self.request.session['emails']

        # Un-serialize JSON email list, back to Python list
        emails_list = json.loads(emails_json, object_hook=email_decoder)
        email_to_display_id = int(self.request.GET["email-id"])
        email_to_display = None
        for email in emails_list:
            if email.id == email_to_display_id:
                email_to_display = email

        context['email'] = email_to_display

        return context


