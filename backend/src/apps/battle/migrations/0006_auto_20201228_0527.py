# Generated by Django 3.1.4 on 2020-12-28 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0005_auto_20201226_0336'),
    ]

    operations = [
        migrations.AddField(
            model_name='battle',
            name='relics',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='battle',
            name='status_effects',
            field=models.JSONField(default=dict),
        ),
    ]