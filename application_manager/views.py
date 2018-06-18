from django.shortcuts import render
from django.views.generic import *
from django.urls import reverse_lazy
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
# This class contains the model name, template name, and context_object_name.
# It's queryset is automatically set to all instances of its model, and it returns
# an HttpResponse with all of the instances of its model
class ApplicationsListView(ListView):
    model = Application
    template_name = "application_manager/index.html"
    context_object_name = 'applications'

# when request.method == GET, returns HttpResponse of template containing empty
# form for its model. When request method is POST, saves it to database, and redirects
# to models absolute url (model.get_absolute_url)
class ApplicationCreate(CreateView):
    model = Application
    fields = APPLICATION_FORM_FIELDS
    template_name_suffix = '-form'

# when request.method == GET, accepts pk parameter, and returns HttpResponse of template containing form
# for its model, populated with its objects values, for editing/updating.
# When request method is POST, saves it to database, and redirects
# to models absolute url (model.get_absolute_url)
class ApplicationUpdate(UpdateView):
    model = Application
    fields = APPLICATION_FORM_FIELDS
    template_name_suffix = '-form'

# when request.method == GET, accepts pk parameter, and returns HttpResponse of template containing
# confirmation for deletion of its object.
# When request method is POST, deletes it from database, and redirects
# to success_url (NOT models absolute url)
class ApplicationDelete(DeleteView):
    model = Application
    fields = APPLICATION_FORM_FIELDS
    template_name_suffix = '-delete-form'
    success_url = reverse_lazy('application_manager:application-list')
