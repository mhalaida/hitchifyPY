# Generated by Django 3.0.6 on 2020-06-15 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hitchify', '0006_auto_20200615_2136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='src_file',
        ),
        migrations.AddField(
            model_name='photo',
            name='url',
            field=models.URLField(default='https://dapp.dblog.org/img/default.jpg'),
        ),
    ]