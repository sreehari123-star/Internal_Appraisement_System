# Generated by Django 4.2.3 on 2023-07-31 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ccsit_internal_mark_app', '0008_rename_login_student_login'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Student_Login',
        ),
    ]
