# Generated by Django 4.2.3 on 2023-08-05 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ccsit_internal_mark_app', '0026_alter_studentregistration_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentregistration',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ccsit_internal_mark_app.student'),
        ),
    ]
