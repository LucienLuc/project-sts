from rest_framework import viewsets

# importing serializers
# from django.contrib.auth import get_user_model
# User = get_user_model()

from rest_framework.decorators import action

# importing models
from rest_framework.response import Response
from src.apps.battle.main.models import Battle
from src.apps.battle.main.serializers import BattleSerializer

from django.shortcuts import get_object_or_404
# lobbies can only be read 

class BattleViewSet(viewsets.ModelViewSet):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer

    # @action(detail=True, methods=['post', 'get'])
    # def foo(self, request, pk):
    #     return Response(status= 200)

    def create(self, request, *args, **kwargs):
        obj = Battle.objects.create()
        return Response(status= 200)
