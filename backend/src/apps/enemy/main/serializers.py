from rest_framework import serializers
from django.db import models
from .models import Enemy

class EnemySerializer(serializers.ModelSerializer):
    ENEMYTYPE = (
        ('rat','rat'),
        ('slime', 'slime'),
    )
    enemy_type = models.CharField(max_length = 7, choices = ENEMYTYPE)
    class Meta:
        model = Enemy
        fields = 'enemy_type'