# Generated by Django 4.2.3 on 2023-08-03 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccsit_internal_mark_app', '0017_send_feedback_delete_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='electivemarks',
            name='elective_marks_saved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='electivemarks',
            name='assignment',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='electivemarks',
            name='attendance',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='electivemarks',
            name='seminar',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='electivemarks',
            name='test1',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='electivemarks',
            name='test2',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='electivemarks',
            name='total_marks',
            field=models.IntegerField(),
        ),
    ]