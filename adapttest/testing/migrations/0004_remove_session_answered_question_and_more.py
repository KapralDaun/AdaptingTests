# Generated by Django 4.0.3 on 2022-04-13 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0003_remove_subject_countofquestions_session_ph_1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='answered_question',
        ),
        migrations.AddField(
            model_name='session',
            name='isFirstQuestion',
            field=models.BooleanField(default=True),
        ),
    ]
