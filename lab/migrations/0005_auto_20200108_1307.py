# Generated by Django 2.2.8 on 2020-01-08 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0004_auto_20200108_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaluser',
            name='is_cnrs',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_cnrs',
        ),
    ]
