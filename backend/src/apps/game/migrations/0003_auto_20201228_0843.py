# Generated by Django 3.1.4 on 2020-12-28 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_game_relic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='relic',
            new_name='relics',
        ),
    ]
