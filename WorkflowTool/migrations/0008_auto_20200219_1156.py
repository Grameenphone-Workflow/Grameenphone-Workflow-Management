# Generated by Django 2.2.6 on 2020-02-19 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkflowTool', '0007_auto_20200219_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpuser',
            name='role',
            field=models.CharField(choices=[('Superadmin', 'Super Admin'), ('KAM', 'KAM'), ('COPC', 'COPC'), ('VA', 'VA'), ('LERP', 'LERP'), ('GERP', 'GERP'), ('CLC', 'CLC'), ('DA', 'DA')], default='KAM', max_length=10),
        ),
    ]
