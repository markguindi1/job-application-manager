# Generated by Django 2.0.3 on 2018-06-11 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application_manager', '0002_auto_20180611_0406'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='one_site',
            new_name='on_site',
        ),
    ]