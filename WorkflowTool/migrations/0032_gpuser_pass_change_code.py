# Generated by Django 2.2.6 on 2020-03-03 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkflowTool', '0031_auto_20200302_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='gpuser',
            name='pass_change_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
