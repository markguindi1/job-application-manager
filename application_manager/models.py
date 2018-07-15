from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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

    def __str__(self):
        return self.company_name + ' (' + self.position + ')'

    def get_absolute_url(self):
        return reverse('application_manager:application-list')


class EmailAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.EmailField()

    def __str__(self):
        return self.address


class Email(models.Model):
    JOB_AD = "Job ad"
    IN_PROGRESS = 'In progress'
    APPLIED = 'Applied'
    INTERVIEWING = "Interviewing"
    ACCEPTANCE = 'Acceptance'
    REJECTION = 'Rejection'
    OFFER_ACCEPTANCE = 'Offer acceptance'
    OFFER_REJECTION = 'Offer rejection'
    TAG_CHOICES = [
        (JOB_AD, "Job ad"),
        (IN_PROGRESS, 'In progress'),
        (APPLIED, 'Applied'),
        (INTERVIEWING, "Interviewing"),
        (ACCEPTANCE, 'Acceptance'),
        (REJECTION, 'Rejection'),
        (OFFER_ACCEPTANCE, "Offer acceptance"),
        (OFFER_REJECTION, 'Offer rejection'),
    ]

    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    email_address = models.ForeignKey(EmailAddress, null=True, on_delete=models.SET_NULL)
    email_link = models.CharField(max_length = 256)
    email_tag = models.CharField(max_length=30, null=True, blank=True, choices=TAG_CHOICES)

    def __str__(self):
        return "Email at {} for {}".format(self.email_address, str(self.application))


class Link(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    link = models.CharField(max_length = 300)

    def __str__(self):
        return "Link for {}".format(str(self.application))


class Note(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    date_created = models.DateTimeField(null=True, blank=True)
    date_last_edited = models.DateTimeField(null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return "Note for {}".format(str(self.application))

class Appointment(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    address_street = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    on_site = models.NullBooleanField(null=True, blank=True)
    note = models.TextField()

    def __str__(self):
        return "Note for {}".format(str(self.application))
