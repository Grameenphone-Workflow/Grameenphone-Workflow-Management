# Generated by Django 2.2.6 on 2020-02-25 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkflowTool', '0022_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productrequisition',
            name='id',
        ),
        migrations.AddField(
            model_name='productrequisition',
            name='deal_closed',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productrequisition',
            name='wfid',
            field=models.CharField(default=2123, max_length=255, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
