# Generated by Django 3.1.4 on 2020-12-28 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enemy', '0007_enemy_status_effects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enemy',
            name='status_effects',
            field=models.JSONField(default=dict),
        ),
    ]
