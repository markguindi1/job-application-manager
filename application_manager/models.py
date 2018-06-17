from django.db import models

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
    STATUS_CHOICES = [
        (NOT_APPLIED, "Didn't apply yet"),
        (IN_PROGRESS, 'In progress'),
        (APPLIED, 'Applied'),
        (INTERVIEWING, "Interviewing"),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (OFFER_ACCEPTED, "Offer accepted")
    ]

    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=25, null=True)
    position_type = models.CharField(max_length=16, null=True, choices=POSITION_TYPE_CHOICES)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=5, null=True)
    country = models.CharField(max_length=20)
    on_site = models.NullBooleanField(null=True)
    application_link = models.CharField(max_length=256, null=True)
    status = models.CharField(max_length=30, null=True, choices=STATUS_CHOICES)
    lead = models.SmallIntegerField()

class Email(models.Model):
    JOB_AD = "Job ad"
    IN_PROGRESS = 'In progress'
    APPLIED = 'Applied'
    INTERVIEWING = "Interviewing"
    ACCEPTANCE = 'Acceptance'
    REJECTION = 'Rejection'
    OFFER_ACCEPTANCE = 'Offer acceptance'
    TAG_CHOICES = [
        (JOB_AD, "Job ad"),
        (IN_PROGRESS, 'In progress'),
        (APPLIED, 'Applied'),
        (INTERVIEWING, "Interviewing"),
        (ACCEPTANCE, 'Acceptance'),
        (REJECTION, 'Rejection'),
        (OFFER_ACCEPTANCE, "Offer acceptance")
    ]

    email_link = models.CharField(max_length = 256)
    email_tag = models.CharField(max_length=30, null=True, choices=TAG_CHOICES)

class Link(models.Model):
    link = models.CharField(max_length = 256)

class Note(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    date_created = models.DateTimeField()
    date_last_edited = models.DateTimeField()
    content = models.TextField()

class Appointment(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    address_street = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=5, null=True)
    country = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    on_site = models.NullBooleanField()
    note = models.TextField()
