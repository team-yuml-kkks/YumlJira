# Generated by Django 2.2.5 on 2019-10-04 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20191004_0711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='project',
        ),
    ]