from rest_framework import serializers
from django.db import models
from .models import Test

class TestSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(max_value = None, min_value = None)
    class Meta:
        model = Test
        fields = '__all__'