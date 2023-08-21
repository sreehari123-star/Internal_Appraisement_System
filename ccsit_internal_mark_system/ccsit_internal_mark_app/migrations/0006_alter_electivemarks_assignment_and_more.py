# Generated by Django 4.2.3 on 2023-07-30 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccsit_internal_mark_app', '0005_rename_elective_marks_electivemarks_assignment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electivemarks',
            name='assignment',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='electivemarks',
            name='attendance',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='electivemarks',
            name='seminar',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='electivemarks',
            name='test1',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='electivemarks',
            name='test2',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='electivemarks',
            name='total_marks',
            field=models.IntegerField(default=0),
        ),
    ]
