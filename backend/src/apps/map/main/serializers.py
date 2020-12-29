from rest_framework import serializers
from django.db import models
from .models import Map

class MapSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(max_value = None, min_value = None)
    class Meta:
        model = Map
        fields = '__all__'