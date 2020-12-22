from rest_framework import viewsets

# importing serializers
# from django.contrib.auth import get_user_model
# User = get_user_model()

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# importing models
from src.apps.enemy.main.models import Enemy
from src.apps.enemy.main.serializers import EnemySerializer

from django.shortcuts import get_object_or_404

from src.enemy.enemy import Enemy as ClassEnemy
from src.enemy.enemies import *

class EnemyViewSet(viewsets.ModelViewSet):
    queryset = Enemy.objects.all()
    serializer_class = EnemySerializer

    @action(detail=True, methods=['post'])
    def next_move(self, request, pk):
        enemy = self.get_object()

        enemy_module = globals()[enemy.enemy_type]
        enemy = getattr(enemy_module, 'Slime')

        print(enemy.name)

        return Response(status=200)

    def create(self, request, *args, **kwargs):
        try:
            enemy_name = request.data['enemy_type']
            enemy_module = globals()[enemy_name.lower()]
            enemy = getattr(enemy_module, enemy_name)
        except:
            return Response(status=404)
        move = enemy.get_next_move(self)
        # obj = Enemy.objects.create(
        #         max_health = enemy.max_health, 
        #         curr_health = enemy.max_health, 
        #         enemy_type = enemy.name.lower(),
        #         )
        # obj.next_move = move
        return Response(status=202)

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]