from django.shortcuts import render
from django.views.generic import *
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from application_manager.models import *

# Create your views here.


class UserCreate(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("homepage:homepage")
    template_name = "registration/register.html"

    def form_valid(self, form):

        # Check for other users with same username
        if User.objects.filter(username=form.cleaned_data['username']).exists():
            username_taken_error = ValidationError("Username already taken", code="username_taken")
            form.add_error('username', username_taken_error)
            return self.form_invalid(form)

        # Login the newly registered user
        # First catch the value of parent class method form_valid() in valid,
        # because when you call it, it calls the form.save(), which registers
        # the user in the database and populates your self.object with the user created.
        valid = super(UserCreate, self).form_valid(form)
        username=form.cleaned_data['username']
        password=form.cleaned_data['password1']
        new_user = authenticate(username=username, password=password, )
        login(self.request, new_user)
        return valid


class ManageAccountView(LoginRequiredMixin, TemplateView):
    template_name = "registration/manage-account.html"


