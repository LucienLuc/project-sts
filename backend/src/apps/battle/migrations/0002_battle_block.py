# Generated by Django 3.1.4 on 2020-12-25 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='battle',
            name='block',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
