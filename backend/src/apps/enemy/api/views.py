from rest_framework import viewsets

# importing serializers
# from django.contrib.auth import get_user_model
# User = get_user_model()

from rest_framework.decorators import action

# importing models
from rest_framework.response import Response
from src.apps.enemy.main.models import Enemy
from src.apps.enemy.main.serializers import EnemySerializer

from django.shortcuts import get_object_or_404
# lobbies can only be read 

class EnemyViewSet(viewsets.ModelViewSet):
    queryset = Enemy.objects.all()
    serializer_class = EnemySerializer

    # @action(detail=True, methods=['post', 'get'])
    # def foo(self, request, pk):
    #     return Response(status= 200)

    def create(self, request, *args, **kwargs):
        print(request.data)
        obj = Enemy.objects.create(number = request.data['number'])
        return Response(status= 200)
