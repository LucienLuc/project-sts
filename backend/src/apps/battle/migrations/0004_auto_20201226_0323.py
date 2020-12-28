# Generated by Django 3.1.4 on 2020-12-26 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0003_auto_20201226_0142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='battle',
            name='buffs',
        ),
        migrations.RemoveField(
            model_name='battle',
            name='debuffs',
        ),
        migrations.AddField(
            model_name='battle',
            name='status_effects',
            field=models.JSONField(default=[]),
            preserve_default=False,
        ),
    ]