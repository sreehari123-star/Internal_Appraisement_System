# Generated by Django 4.2.3 on 2023-08-05 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ccsit_internal_mark_app', '0027_alter_studentregistration_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentregistration',
            old_name='elective_subject',
            new_name='elective_subjects',
        ),
    ]
