# Generated by Django 3.0.6 on 2020-05-06 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hitchify', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hitchspot',
            name='update_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
