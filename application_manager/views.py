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

APPLICATION_FORM_FIELDS = ['company_name',
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

class UserCreate(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("homepage:homepage")
    template_name = "registration/register.html"

    def form_valid(self, form):

        other_users_same_username = User.objects.all().filter(username=form.cleaned_data['username'])
        if len(other_users_same_username) > 0:
            username_taken_error = ValidationError("Username already taken", code="username_taken")
            form.add_error('username', username_taken_error)
            return self.form_invalid(form)

        # First catch the value of parent class method form_valid() in valid,
        # because when you call it, it calls the form.save(), which registers
        # the user in the database and populates your self.object with the user created.
        valid = super(UserCreate, self).form_valid(form)
        username=form.cleaned_data['username']
        password=form.cleaned_data['password1']
        new_user = authenticate(username=username, password=password, )
        login(self.request, new_user)
        return valid


# This class contains the model name, template name, and context_object_name.
# It's queryset is automatically set to all instances of its model, and it returns
# an HttpResponse with all of the instances of its model
class ApplicationsListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = "application_manager/index.html"
    context_object_name = 'applications'

    def get_queryset(self):
        queryset = Application.objects.all().filter(user=self.request.user)
        return queryset

# when request.method == GET, returns HttpResponse of template containing empty
# form for its model. When request method is POST, saves it to database, and redirects
# to models absolute url (model.get_absolute_url)
class ApplicationCreate(LoginRequiredMixin, CreateView):
    model = Application
    fields = APPLICATION_FORM_FIELDS
    template_name_suffix = '-form'

    # Overriden in order to set the new application's user to the current user
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

    # Overriden in order to set the updated application's user to the current user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# when request.method == GET, accepts pk parameter, and returns HttpResponse of template containing
# confirmation for deletion of its object.
# When request method is POST, deletes it from database, and redirects
# to success_url (NOT models absolute url)
class ApplicationDelete(LoginRequiredMixin, DeleteView):
    model = Application
    fields = APPLICATION_FORM_FIELDS
    template_name_suffix = '-delete-form'
    success_url = reverse_lazy('application_manager:application-list')
