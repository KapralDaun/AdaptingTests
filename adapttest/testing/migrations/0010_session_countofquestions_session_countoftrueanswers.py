# Generated by Django 4.0.3 on 2022-05-13 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0009_remove_session_countofquestions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='countOfQuestions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='session',
            name='countOfTrueAnswers',
            field=models.IntegerField(default=0),
        ),
    ]
