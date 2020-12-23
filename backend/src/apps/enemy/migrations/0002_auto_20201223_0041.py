# Generated by Django 3.1.4 on 2020-12-23 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enemy', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enemy',
            old_name='enemy_type',
            new_name='enemy_name',
        ),
        migrations.AddField(
            model_name='enemy',
            name='next_move',
            field=models.JSONField(default=dict),
        ),
    ]
