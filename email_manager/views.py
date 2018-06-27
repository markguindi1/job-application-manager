from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.core import serializers
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
        # get email, pswd, since_date, use them to get emails
        email = form.cleaned_data['email']
        pswd = form.cleaned_data['password']
        date_from = form.cleaned_data['emails_since']
        emails_list = get_emails(email, pswd, date_from)
        print("In form_valid: got list of emails")
        emails_json = json.dumps([email.__dict__ for email in emails_list])
        print("In form_valid: JSON-serialized list of emails")
        #serialized_obj = serializers.serialize('json', emails)
        # add emails to session
        self.request.session['emails'] = emails_json
        print("In form_valid: JSON-serialized emails added to session")
        #self.request.session['email-valid'] = True
        # return Httpresponse:
        return super().form_valid(form)

class EmailsListView(TemplateView):
    template_name = "email_manager/emails-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emails_json = self.request.session['emails']
        print("In redirect to EmailsListView: got emails list from session")
        emails_list = json.loads(emails_json)
        print("In redirect to EmailsListView: unserialized JSON to Python")
        context['emails'] = emails_list
        print("In redirect to EmailsListView: added emails to context")
        return context
