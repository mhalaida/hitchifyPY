# Generated by Django 3.0.6 on 2020-06-10 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hitchify', '0002_photo_src_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='url',
        ),
    ]
