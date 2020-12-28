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

# from ....card.cards import *
# from ....card.card import Card

from src.card.cards import *
from src.card.card import Card, CardEncoder
# from src.relic.relic import 
import json

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(detail=True, methods=['post'])
    def add_card_to_deck(self, request, pk):
        try:
            card_name = request.data['card_name'].replace(' ', '')
            card_module = globals()[card_name.lower()]
            card = getattr(card_module, card_name)
        except:
            return Response(status=404)
        game = self.get_object()
        card_json = json.dumps(card, cls = CardEncoder)
        game.deck.append(card_json)
        game.save()
        return Response(status=200)

    @action(detail=True, methods=['post'])
    def remove_card_from_deck(self, request, pk):
        try:
            card_name = request.data['card_name'].replace(' ', '')
            card_module = globals()[card_name.lower()]
            card = getattr(card_module, card_name)
        except:
            return Response(status=404)
        game = self.get_object()
        card_json = json.dumps(card, cls = CardEncoder)
        try:
            game.deck.remove(card_json)
        except:
            return Response(status=404)
        game.save()
        return Response(status=200)    

    @action(detail=True, methods=['post'])
    def add_relic(self, request, pk):
        try:
            card_name = request.data['card_name'].replace(' ', '')
            card_module = globals()[card_name.lower()]
            card = getattr(card_module, card_name)
        except:
            return Response(status=404)
        game = self.get_object()
        card_json = json.dumps(card, cls = CardEncoder)
        game.deck.append(card_json)
        game.save()
        return Response(status=200)

    @action(detail=True, methods=['post'])
    def remove_relic(self, request, pk):
        try:
            card_name = request.data['card_name'].replace(' ', '')
            card_module = globals()[card_name.lower()]
            card = getattr(card_module, card_name)
        except:
            return Response(status=404)
        game = self.get_object()
        card_json = json.dumps(card, cls = CardEncoder)
        game.deck.append(card_json)
        game.save()
        return Response(status=200)

    @action(detail=True, methods=['get'])
    def get_deck(self, request, pk):
        game = self.get_object()
        return Response(data = game.deck, status=200) 

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, id = serializer.validated_data['id'])
            #Link user to Game object - every game MUST have a user
            game = Game.objects.create(
            max_health = 100, 
            curr_health = 100,
            max_mana = 3,
            gamestate = 'map', 
            gold = 0,
            # deck = list, 
            user = user, 
            id = user.id)
            return Response(status=200)
        return Response(status=400)

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create', 'list', 'retrieve', 'add_card_to_deck', 'remove_card_from_deck', 'get_deck']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]