from rest_framework import viewsets

# from django.contrib.auth import get_user_model
# User = get_user_model()

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# Models and Serializers
from rest_framework.response import Response
from src.apps.game.main.models import Game
from src.apps.game.main.serializers import GameSerializer

# from src.apps.myauth.main.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from src.apps.myauth.main.serializers import UserSerializer

from django.shortcuts import get_object_or_404

from ....card.cards import *
from ....card.card import Card

from types import MappingProxyType
import json
class CardEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, MappingProxyType):
            return {
                "name": obj['name'],
                "description": obj['description'],
                "mana": obj['mana']
            }
        return json.JSONEncoder.default(self, obj)

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    # @action(detail=True, methods=['post', 'get'])
    # def foo(self, request, pk):
    #     return Response(status= 200)

    @action(detail=True, methods=['post'])
    def add_card_to_deck(self, request, pk):
        try:
            card_name = request.data['card_name']
            card_module = globals()[card_name.lower()]
            card = getattr(card_module, card_name)
        except:
            return Response(status=404)
        game = self.get_object()
        game.deck.append(card)
        return Response(status=200)

    @action(detail=True, methods=['post'])
    def remove_card_from_deck(self, request, pk):
        try:
            card_name = request.data['card_name']
            card_module = globals()[card_name.lower()]
            card = getattr(card_module, card_name)
        except:
            return Response(status=404)
        game = self.get_object()
        game.deck.remove(card)
        return Response(status=200)    

    @action(detail=True, methods=['get'])
    def get_deck(self, request, pk):
        game = self.get_object()
        deck = []
        for i in range(len(game.deck)):
            deck.append(json.dumps(game.deck[i].__dict__, cls=CardEncoder))
        return Response(data=deck, status=200) 

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, id = serializer.validated_data['id'])
            #Link user to Game object - every game MUST have a user
            game = Game.objects.create(max_health = 100, curr_health = 100, gamestate = 'map', gold = 0, user = user, id = user.id)
            return Response(status=200)
        return Response(status=400)

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create', 'list', 'retrieve', 'add_card_to_deck', 'remove_card_from_deck', 'get_deck']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]