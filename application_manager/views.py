from django.shortcuts import render
from django.views.generic import *
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *
from .tables import *
# Create your views here.


APPLICATION_FORM_FIELDS = [
        'company_name',
        'position',
        'position_type',
        'city',
        'state',
        'country',
        'on_site',
        'application_link',
        'status',
        'lead'
]


class HomepageView(TemplateView):
    template_name = "application_manager/base.html"


# This class contains the model name, template name, and context_object_name.
# It's queryset is all the user's job applications (default is all instances of its model), and it returns
# an HttpResponse with all of the instances of its model
class ApplicationsListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = "application_manager/index.html"
    context_object_name = 'applications'

    def get_queryset(self):
        queryset = super(ApplicationsListView, self).get_queryset().filter(user=self.request.user)
        return queryset


# when request.method == GET, returns HttpResponse of template containing empty
# form for its model. When request method is POST, saves it to database, and redirects
# to models absolute url (model.get_absolute_url)
class ApplicationCreate(LoginRequiredMixin, CreateView):
    model = Application
    fields = APPLICATION_FORM_FIELDS
    template_name_suffix = '-form'

    # Overridden in order to set the new application's user to the current user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# when request.method == GET, accepts pk parameter, and returns HttpResponse of template containing form
# for its model, populated with its objects values, for editing/updating.
# When request method is POST, saves it to database, and redirects
# to models absolute url (model.get_absolute_url)
class ApplicationUpdate(LoginRequiredMixin, UpdateView):
    model = Application
    fields = APPLICATION_FORM_FIELDS
    template_name_suffix = '-form'

    # Overridden in order to confirm that the request is coming from the owner of this resource
    def get_queryset(self):
        return super(ApplicationUpdate, self).get_queryset().filter(user=self.request.user)


# when request.method == GET, accepts pk parameter, and returns HttpResponse of template containing
# confirmation for deletion of its object.
# When request method is POST, deletes it from database, and redirects
# to success_url (NOT models absolute url)
class ApplicationDelete(LoginRequiredMixin, DeleteView):
    model = Application
    fields = APPLICATION_FORM_FIELDS
    template_name_suffix = '-delete-form'
    success_url = reverse_lazy('application_manager:application_list')

    # Overridden in order to confirm that the request is coming from the owner of this resource
    def get_queryset(self):
        return super(ApplicationDelete, self).get_queryset().filter(user=self.request.user)
