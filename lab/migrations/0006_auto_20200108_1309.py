# Generated by Django 2.2.8 on 2020-01-08 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0005_auto_20200108_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproject',
            name='is_cnrs',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='project',
            name='is_cnrs',
            field=models.BooleanField(default=True),
        ),
    ]
