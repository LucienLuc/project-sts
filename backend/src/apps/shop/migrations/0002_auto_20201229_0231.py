# Generated by Django 3.1.4 on 2020-12-29 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='card1',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='card2',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='card3',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='relic1',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='relic2',
            field=models.JSONField(default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='relic3',
            field=models.JSONField(default=dict, null=True),
        ),
    ]
