# Generated by Django 3.1.4 on 2020-12-22 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20201222_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='deck',
            field=models.JSONField(default=list),
        ),
    ]
