# Generated by Django 4.2.5 on 2023-10-20 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_remove_task_if_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='deadline',
        ),
    ]
