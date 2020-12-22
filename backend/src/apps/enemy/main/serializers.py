from rest_framework import serializers
from django.db import models
from .models import Enemy

class EnemySerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(max_value = None, min_value = None)
    class Meta:
        model = Enemy
        fields = '__all__'