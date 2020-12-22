from rest_framework import serializers

# from .models import User
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
# from src.apps.myauth.main.models import User

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    class Meta:
        model = User
        fields = '__all__'
        lookup_field = 'id'
        