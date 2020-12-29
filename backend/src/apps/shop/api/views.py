from rest_framework import viewsets

# importing serializers
# from django.contrib.auth import get_user_model
# User = get_user_model()
from django.forms.models import model_to_dict
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# importing models
from rest_framework.response import Response
from src.apps.shop.main.models import Shop
from src.apps.shop.main.serializers import ShopSerializer
from src.apps.game.main.models import Game
from src.apps.game.main.serializers import GameSerializer

from src.card.cards import *
from src.card.card import Card, CardEncoder, COMMON_CARD_POOL, UNCOMMON_CARD_POOL, RARE_CARD_POOL
from src.relic.relic import COMMON_RELIC_POOL, UNCOMMON_RELIC_POOL, RARE_RELIC_POOL, SHOP_RELIC_POOL, RELIC_DICT

from django.shortcuts import get_object_or_404

import random
import json

COMMON_CARD_LEN = len(COMMON_CARD_POOL)
UNCOMMON_CARD_LEN = len(UNCOMMON_CARD_POOL)
RARE_CARD_LEN = len(RARE_CARD_POOL)

# COMMON_RELIC_LEN = len(COMMON_RELIC_POOL)
# UNCOMMON_RELIC_LEN = len(UNCOMMON_RELIC_POOL)
# RARE_RELIC_LEN = len(RARE_RELIC_POOL)
# SHOP_RELIC_LEN = len(SHOP_RELIC_POOL)

def generate_cards():
    return [COMMON_CARD_POOL[random.randint(0, COMMON_CARD_LEN-1)], 
    UNCOMMON_CARD_POOL[random.randint(0, UNCOMMON_CARD_LEN-1)],
    RARE_CARD_POOL[random.randint(0, RARE_CARD_LEN-1)]]

def generate_relics(curr_relics):
    selector = random.randint(0,1)
    NEW_COMMON_RELIC_POOL = list(set(COMMON_RELIC_POOL) - curr_relics)
    NEW_UNCOMMON_RELIC_POOL = list(set(UNCOMMON_RELIC_POOL) - curr_relics)
    NEW_RARE_RELIC_POOL = list(set(RARE_RELIC_POOL) - curr_relics)
    NEW_SHOP_RELIC_POOL = list(set(SHOP_RELIC_POOL) - curr_relics)
    if selector == 0:
        return [NEW_COMMON_RELIC_POOL[random.randint(0, len(NEW_COMMON_RELIC_POOL)-1)], 
        NEW_UNCOMMON_RELIC_POOL[random.randint(0, len(NEW_UNCOMMON_RELIC_POOL)-1)],
        NEW_RARE_RELIC_POOL[random.randint(0, len(NEW_RARE_RELIC_POOL)-1)]
        ]
    else:
        return [NEW_COMMON_RELIC_POOL[random.randint(0, len(NEW_COMMON_RELIC_POOL)-1)], 
        NEW_UNCOMMON_RELIC_POOL[random.randint(0, len(NEW_UNCOMMON_RELIC_POOL)-1)],
        NEW_SHOP_RELIC_POOL[random.randint(0, len(NEW_SHOP_RELIC_POOL)-1)]
        ]
        
class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    @action(detail=True, methods=['post'])
    def leave(self, request, pk):
        game_serializer = GameSerializer(data=request.data)
        if game_serializer.is_valid():
            shop = self.get_object()
            game = get_object_or_404(Game, id=game_serializer.validated_data['id'])
            game.gamestate = 'map'
            shop.delete()
            return Response(status=200)
        return Response(status=400)

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk):
        game_serializer = GameSerializer(data=request.data)
        if game_serializer.is_valid():
            game = get_object_or_404(Game, id=game_serializer.validated_data['id'])
            shop = self.get_object()
            try:
                selection_cost = request.data['selection'] + '_cost'
                cost = getattr(shop, selection_cost)

                # CHANGE
                if game.gold > cost:
                    return Response(status=409)
                item = getattr(shop, request.data['selection'])
                
                #remove last char

                #potions in the shop?

                item_type = request.data['selection'][:-1]
                if item_type == 'card':
                    game.deck.append(item)
                elif item_type == 'relic':
                    game.relics.update(item)
                setattr(shop, request.data['selection'], None)
            except:
                return Response(status=400)
            game.save()
            shop.save()
            return Response(status=200)
        # print(shop_serializer.errors)
        return Response(status=400)

    @action(detail=True, methods=['get'])
    def get_state(self, request, pk):
        shop = self.get_object()
        obj = model_to_dict(shop)
        return Response(data=obj, status=200)

    def create(self, request, *args, **kwargs):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            game = get_object_or_404(Game, id=serializer.validated_data['id'])
            shop_cards = generate_cards()
            cards_json = []
            for item in shop_cards:
                try:
                    card_module = globals()[item.lower().replace(' ', '')]
                    card = getattr(card_module, item.title().replace(' ', ''))
                except:
                    return Response(status=404)
                cards_json.append(json.dumps(card, cls=CardEncoder))

            current_relics = set(game.relics.keys())
            shop_relics = generate_relics(current_relics)

            shop = Shop.objects.create(
                game = game,
                card1 = cards_json[0],
                card2 = cards_json[1],
                card3 = cards_json[2],
                card1_cost = random.randint(40,50),
                card2_cost = random.randint(80,110),
                card3_cost = random.randint(150,200),

                relic1 = {shop_relics[0].title(): RELIC_DICT[shop_relics[0].title()]},
                relic2 = {shop_relics[1].title(): RELIC_DICT[shop_relics[1].title()]},
                relic3 = {shop_relics[2].title(): RELIC_DICT[shop_relics[2].title()]},
                relic1_cost = random.randint(70,100),
                relic2_cost = random.randint(120,150),
                relic3_cost = random.randint(200,250),

                id = game.id
            )
            return Response(status=201)
        return Response(status=404)

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create', 'list', 'retrieve' ,'get_state', 'leave', 'purchase']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]