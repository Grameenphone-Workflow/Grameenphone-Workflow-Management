# Generated by Django 2.2.6 on 2020-04-11 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldops', '0006_visit_visit_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='visit_image_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
