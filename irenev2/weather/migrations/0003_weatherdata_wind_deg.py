# Generated by Django 5.1.6 on 2025-02-15 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_weatherdata_air_quality_weatherdata_sunrise_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='weatherdata',
            name='wind_deg',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
