# Generated by Django 4.2.3 on 2023-08-05 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ccsit_internal_mark_app', '0030_rename_elective_subjects_studentregistration_elective_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='electivemarks',
            name='elective_course',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to='ccsit_internal_mark_app.electivecourse'),
            preserve_default=False,
        ),
    ]
