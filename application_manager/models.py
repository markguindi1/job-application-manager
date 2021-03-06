from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# from oauth2client.contrib.django_util.models import CredentialsField

# Create your models here.


class Application(models.Model):
    FULLTIME = 'Full-time'
    PARTTIME = 'Part-time'
    INTERNSHIP = 'Internship'
    PARTTIME_INTERNSHIP = 'Part-time intership'
    POSITION_TYPE_CHOICES = [
        (FULLTIME, 'Full-time'),
        (PARTTIME, 'Part-time'),
        (INTERNSHIP, 'Internship'),
        (PARTTIME_INTERNSHIP, 'Part-time intership'),
    ]

    NOT_APPLIED = "Didn't apply yet"
    IN_PROGRESS = 'In progress'
    APPLIED = 'Applied'
    INTERVIEWING = "Interviewing"
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    OFFER_ACCEPTED = 'Offer accepted'
    OFFER_REJECTED = 'Offer rejected'
    STATUS_CHOICES = [
        (NOT_APPLIED, "Didn't apply yet"),
        (IN_PROGRESS, 'In progress'),
        (APPLIED, 'Applied'),
        (INTERVIEWING, "Interviewing"),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (OFFER_ACCEPTED, "Offer accepted"),
        (OFFER_REJECTED, "Offer rejected"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=40, null=True, blank=True)
    position_type = models.CharField(max_length=25, null=True, blank=True, choices=POSITION_TYPE_CHOICES)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20)
    on_site = models.NullBooleanField(null=True, blank=True)
    application_link = models.CharField(max_length=256, null=True, blank=True)
    status = models.CharField(max_length=30, null=True, blank=True, choices=STATUS_CHOICES)
    lead = models.SmallIntegerField()
    email_tag = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.company_name + ' (' + self.position + ')'

    def get_absolute_url(self):
        return reverse('application_manager:application_list')


class EmailAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.EmailField()
    last_checked_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.address

    def get_absolute_url():
        return reverse('email_manager:emails_addresses_list')


class CustomStateModel(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    state = models.CharField(max_length=30)


class CustomCredentialsModel(models.Model):

    def __init__(self, user, flow_credentials):
        self.user = user
        self.token = flow_credentials.token
        self.refresh_token = flow_credentials.refrsh_token
        self.token_uri = flow_credentials.token_uri
        self.client_id = flow_credentials.client_id
        self.client_secret = flow_credentials.client_secret
        self.scopes = flow_credentials.scopes

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    token = models.CharField(max_length=60)
    refresh_token = models.CharField(max_length=60)
    token_uri = models.CharField(max_length=150)
    client_id = models.CharField(max_length=60)
    client_secret = models.CharField(max_length=60)
    scopes = models.CharField(max_length=60)
