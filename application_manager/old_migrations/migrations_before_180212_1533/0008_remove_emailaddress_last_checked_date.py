# Generated by Django 2.0.3 on 2018-08-12 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application_manager', '0007_auto_20180812_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailaddress',
            name='last_checked_date',
        ),
    ]