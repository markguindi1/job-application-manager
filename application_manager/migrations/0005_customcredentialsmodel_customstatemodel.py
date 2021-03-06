# Generated by Django 2.0.3 on 2018-12-27 23:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('application_manager', '0004_auto_20181225_1618'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomCredentialsModel',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('token', models.CharField(max_length=60)),
                ('refresh_token', models.CharField(max_length=60)),
                ('token_uri', models.CharField(max_length=150)),
                ('client_id', models.CharField(max_length=60)),
                ('client_secret', models.CharField(max_length=60)),
                ('scopes', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='CustomStateModel',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('state', models.CharField(max_length=30)),
            ],
        ),
    ]
