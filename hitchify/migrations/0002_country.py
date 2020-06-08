# Generated by Django 3.0.6 on 2020-06-04 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hitchify', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_id', models.IntegerField(primary_key=True, serialize=False)),
                ('country_name', models.CharField(max_length=255)),
                ('short_description', models.CharField(max_length=255)),
                ('national_currency', models.CharField(max_length=255)),
            ],
        ),
    ]