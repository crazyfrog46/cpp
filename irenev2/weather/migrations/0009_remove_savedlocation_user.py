# Generated by Django 5.1.6 on 2025-03-11 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0008_savedlocation_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savedlocation',
            name='user',
        ),
    ]
