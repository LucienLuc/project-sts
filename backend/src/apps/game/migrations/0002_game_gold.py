# Generated by Django 3.1.4 on 2020-12-22 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='gold',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
