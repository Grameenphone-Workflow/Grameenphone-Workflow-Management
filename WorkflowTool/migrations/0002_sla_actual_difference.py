# Generated by Django 2.2.6 on 2020-02-18 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkflowTool', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sla',
            name='actual_difference',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
