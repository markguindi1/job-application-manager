# Generated by Django 2.0.3 on 2018-06-12 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application_manager', '0003_auto_20180611_0406'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='note',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]