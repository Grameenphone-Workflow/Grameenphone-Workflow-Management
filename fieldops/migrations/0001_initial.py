# Generated by Django 2.2.6 on 2020-03-18 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('visit_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('kam_id', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('data_of_visit', models.DateTimeField(blank=True, null=True)),
                ('visited', models.BooleanField()),
            ],
        ),
    ]
