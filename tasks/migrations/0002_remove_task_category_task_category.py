# Generated by Django 4.2.5 on 2023-09-11 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='category',
        ),
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.ManyToManyField(to='tasks.category'),
        ),
    ]
