# Generated by Django 2.0.3 on 2018-07-05 02:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application_manager', '0010_auto_20180617_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]