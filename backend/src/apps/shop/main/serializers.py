from rest_framework import serializers
from django.db import models
from .models import Shop

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'