from rest_framework import serializers
from django.db import models
from .models import Reward

class RewardSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(max_value = None, min_value = None)
    class Meta:
        model = Reward
        fields = '__all__'