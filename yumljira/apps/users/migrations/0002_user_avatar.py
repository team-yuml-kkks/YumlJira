# Generated by Django 2.2.5 on 2019-09-20 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='avatars/'),
        ),
    ]
