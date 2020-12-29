# Generated by Django 3.1.4 on 2020-12-28 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('game', '0003_auto_20201228_0843'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card1', models.JSONField(default=dict)),
                ('card2', models.JSONField(default=dict)),
                ('card3', models.JSONField(default=dict)),
                ('card1_cost', models.IntegerField()),
                ('card2_cost', models.IntegerField()),
                ('card3_cost', models.IntegerField()),
                ('relic1', models.JSONField(default=dict)),
                ('relic2', models.JSONField(default=dict)),
                ('relic3', models.JSONField(default=dict)),
                ('relic1_cost', models.IntegerField()),
                ('relic2_cost', models.IntegerField()),
                ('relic3_cost', models.IntegerField()),
                ('game', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='game.game')),
            ],
        ),
    ]