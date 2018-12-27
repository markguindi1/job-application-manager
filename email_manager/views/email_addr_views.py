from django.urls import reverse_lazy
from django.views.generic import *
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import *
from ..get_emails import *
from ..get_emails_api import *
from ..forms import *
from ..gmail_api_auth_files import authentication_views
from email_manager.old_gmail_api_auth_files.api_emails_list import *
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
    fields = ["address", "last_checked_date"]
    template_name = "email_manager/email-address-form.html"
    success_url = reverse_lazy("email_manager:email_address_list")

    # Overriden so the "last_checked_date" widget is an HTML date input field
    def get_form(self, form_class=None):
        form = super(EmailAccountCreate, self).get_form()
        form.fields['last_checked_date'].widget = CustomDateInput()
        return form

    # Overridden in order to set the new application's user to the current user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EmailAccountUpdate(LoginRequiredMixin, UpdateView):
    model = EmailAddress
    fields = ["address", "last_checked_date"]
    template_name = "email_manager/email-address-form.html"
    success_url = reverse_lazy("email_manager:email_address_list")

    # Overriden so the "last_checked_date" widget is an HTML date input field
    def get_form(self, form_class=None):
        form = super(EmailAccountUpdate, self).get_form()
        form.fields['last_checked_date'].widget = CustomDateInput()
        return form

    def get_queryset(self):
        return super(EmailAccountUpdate, self).get_queryset().filter(user=self.request.user)


class EmailAccountDelete(LoginRequiredMixin, DeleteView):
    model = EmailAddress
    # fields = ["address"]
    template_name = "email_manager/email-address-delete-form.html"
    success_url = reverse_lazy("email_manager:email_address_list")

    def get_queryset(self):
        return super(EmailAccountDelete, self).get_queryset().filter(user=self.request.user)
