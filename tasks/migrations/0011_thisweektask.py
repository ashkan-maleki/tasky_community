# Generated by Django 3.1.3 on 2020-11-27 17:40

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_auto_20201127_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThisWeekTask',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('tasks.task',),
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]
