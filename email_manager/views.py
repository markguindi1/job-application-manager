from django.urls import reverse_lazy
from django.views.generic import *
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .get_emails import *
from .get_emails_api import *
from .forms import *
from .gmail_api_auth_files import authentication_views
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


class EmailFormView(LoginRequiredMixin, FormView):
    template_name = "email_manager/email-form.html"
    success_url = reverse_lazy('email_manager:email_list')

    def get_form_class(self):
        # if emails are retrieved from the Gmail API, password is unnecessary
        if self.email_from_api:
            return ApiEmailForm
        return EmailForm

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)

        if self.email_addr is not None:
            form.initial = {"gmail_email": self.email_addr}
            # if email; address is found in database, pre-populate 'Emails Since'
            # field with 'Last Checked Date' field value
            try:
                email_addr_object = EmailAddress.objects.get(address=self.email_addr)
                form.initial["emails_since"] = email_addr_object.last_checked_date
            except Exception as e:
                pass

        context['form'] = form
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        # Check if emails can be retrieved from API or not.
        # If yes, use ApiEmailForm and get emails from API,
        # otherwise use EmailForm and get emails using plain Python libraries.

        if not CustomCredentialsModel.objects.filter(user=request.user).exists():
            return authentication_views.authorize(request)

        # To do: clean up
        try:
            self.email_addr = self.request.GET["email_addr"]
            self.email_from_api = self.email_addr in GMAIL_API_EMAILS
        except KeyError:
            self.email_addr = None
            self.email_from_api = False

        return super(EmailFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Get email, pswd, since_date, use them to get emails
        email_address = form.cleaned_data['gmail_email']
        if not self.email_from_api:
            pswd = form.cleaned_data['password']
        else:
            pswd = ""
        date_from = form.cleaned_data['emails_since']

        # If authentication fails, redirect to email login page with prepopulated form
        # (by returning self.form_invalid(form)) and display "Invalid credentials" error message
        try:
            if self.email_from_api:
                emails_list = get_emails_api(email_address, date_from)
            else:
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
        email_to_display_id = self.request.GET["email-id"]
        email_to_display = None
        for email in emails_list:
            if email.id == email_to_display_id:
                email_to_display = email

        context['email'] = email_to_display

        return context


