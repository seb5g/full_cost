# Generated by Django 2.2.8 on 2019-12-20 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='experiment',
            field=models.CharField(default='', max_length=200),
        ),
    ]