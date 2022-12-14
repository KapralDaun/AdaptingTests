# Generated by Django 4.0.3 on 2022-04-12 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['question'], 'verbose_name': 'Ответ', 'verbose_name_plural': 'Ответы'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['subject'], 'verbose_name': 'Вопрос', 'verbose_name_plural': 'Вопросы'},
        ),
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ['user'], 'verbose_name': 'Сеанс', 'verbose_name_plural': 'Сеансы'},
        ),
        migrations.AlterField(
            model_name='session',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='testing.subject'),
        ),
    ]
