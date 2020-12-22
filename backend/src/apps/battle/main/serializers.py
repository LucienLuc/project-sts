from rest_framework import serializers
from django.db import models
from .models import Battle

class BattleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Battle
        fields = ['id']