# Generated by Django 2.2.6 on 2020-04-06 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldops', '0002_auto_20200406_0249'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
