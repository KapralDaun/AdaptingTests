# Generated by Django 4.0.3 on 2022-04-24 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0005_alter_session_isfirstquestion'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='answered_question',
            field=models.CharField(default='', max_length=255),
        ),
    ]
