from rest_framework import serializers
from django.db import models
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Game
        fields = ['id']
