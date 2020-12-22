from rest_framework import serializers
from django.db import models
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    health = serializers.IntegerField(max_value = None, min_value = None)
    class Meta:
        model = Game
        fields = '__all__'
