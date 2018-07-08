# Generated by Django 2.0.3 on 2018-06-12 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application_manager', '0004_appointment_note'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='timestamp',
            new_name='date_created',
        ),
        migrations.AddField(
            model_name='note',
            name='date_last_edited',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='application_link',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='position',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='position_type',
            field=models.CharField(choices=[('Full-time', 'Full-time'), ('Part-time', 'Part-time'), ('Internship', 'Internship'), ('Part-time intership', 'Part-time intership'), (None, None)], max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[("Didn't apply yet", "Didn't apply yet"), ('In progress', 'In progress'), ('Applied', 'Applied'), ('Rejected', 'Rejected')], max_length=16),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='address_street',
            field=models.CharField(max_length=30, null=True),
        ),
    ]