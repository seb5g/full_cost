# Generated by Django 2.2.8 on 2019-12-20 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0002_auto_20191220_1107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalproject',
            name='gestionnaire',
        ),
        migrations.RemoveField(
            model_name='project',
            name='gestionnaire',
        ),
        migrations.AlterField(
            model_name='historicalproject',
            name='project_pi',
            field=models.ForeignKey(blank=True, db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lab.User'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_pi',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lab.User'),
        ),
    ]