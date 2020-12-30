from rest_framework import serializers
from django.db import models
from .models import Map

class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = '__all__'

class MoveSerializer(serializers.Serializer):
    next_position = serializers.IntegerField()