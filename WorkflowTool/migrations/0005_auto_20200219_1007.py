# Generated by Django 2.2.6 on 2020-02-19 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkflowTool', '0004_sla_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sla',
            name='actual_difference',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sla',
            name='completion_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sla',
            name='user_identifier',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
