from rest_framework import viewsets

# importing serializers
# from django.contrib.auth import get_user_model
# User = get_user_model()

from rest_framework.decorators import action

# importing models
from rest_framework.response import Response
from src.apps.reward.main.models import Reward
from src.apps.reward.main.serializers import RewardSerializer
from src.apps.game.main.models import Game
from src.apps.game.main.serializers import GameSerializer
from src.card.cards import *
from src.card.card import Card, CardEncoder, COMMON_CARD_POOL, UNCOMMON_CARD_POOL, RARE_CARD_POOL, BOSS_CARD_POOL
from src.relic.relic import COMMON_RELIC_POOL, UNCOMMON_RELIC_POOL, RARE_RELIC_POOL, BOSS_RELIC_POOL, RELIC_DICT

from django.shortcuts import get_object_or_404
import random

COMMON_CARD_LEN = len(COMMON_CARD_POOL)
UNCOMMON_CARD_LEN = len(UNCOMMON_CARD_POOL)
RARE_CARD_LEN = len(RARE_CARD_POOL)
BOSS_CARD_POOL = len(BOSS_CARD_POOL)

COMMON_RELIC_LEN = len(COMMON_RELIC_POOL)
UNCOMMON_RELIC_LEN = len(UNCOMMON_RELIC_POOL)
RARE_RELIC_LEN = len(RARE_RELIC_POOL)
BOSS_RELIC_LEN = len(BOSS_RELIC_POOL)
# SHOP_RELIC_LEN = len(SHOP_RELIC_POOL)

# Probably don't generate duplicate cards in reward screen
def generate(curr_relics, flag):
    NEW_COMMON_RELIC_POOL = list(set(COMMON_RELIC_POOL) - curr_relics)
    NEW_UNCOMMON_RELIC_POOL = list(set(UNCOMMON_RELIC_POOL) - curr_relics)
    NEW_RARE_RELIC_POOL = list(set(RARE_RELIC_POOL) - curr_relics)

    cards = []
    gold = 0
    relic = {}
    if flag == 'boss':
        gold = random.randint(80,120)
    elif flag == 'normal':
        gold = random.randint(20,40)
        # 3 cards
        for i in range(2):
            selector = random.randint(0,3)
            if selector == 0:
                cards.append(UNCOMMON_CARD_POOL[random.randint(0,UNCOMMON_CARD_LEN-1)])
            else:
                cards.append(COMMON_CARD_POOL[random.randint(0,COMMON_CARD_LEN-1)])
        selector = random.randint(0,5)
        if selector == 0:
            cards.append(RARE_CARD_POOL[random.randint(0,RARE_CARD_LEN-1)])
        else:
            cards.append(UNCOMMON_CARD_POOL[random.randint(0,UNCOMMON_CARD_LEN-1)])
    elif flag == 'elite':
        gold = random.randint(50,80)
        for i in range(2):
            selector = random.randint(0,3)
            if selector == 0:
                cards.append(UNCOMMON_CARD_POOL[random.randint(0,UNCOMMON_CARD_LEN-1)])
            else:
                cards.append(RARE_CARD_POOL[random.randint(0,RARE_CARD_LEN-1)])
            cards.append(RARE_CARD_POOL[random.randint(0,RARE_CARD_LEN-1)])
        selector = random.randint(0,1)
        if selector == 0:
            length = len(NEW_RARE_RELIC_POOL)
            new_relic = NEW_RARE_RELIC_POOL[random.randint(0,length-1)].title()
            relic.update({new_relic : RELIC_DICT[new_relic]})
        else:
            length = len(NEW_UNCOMMON_RELIC_POOL)
            new_relic = NEW_UNCOMMON_RELIC_POOL[random.randint(0,length-1)].title()
            relic.update({new_relic : RELIC_DICT[new_relic]})
    return cards, relic, gold

class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

    # @action(detail=True, methods=['post', 'get'])
    # def foo(self, request, pk):
    #     return Response(status= 200)

    def create(self, request, *args, **kwargs):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            game = get_object_or_404(Game, id=serializer.validated_data['id'])
            cards, relic, gold = generate(game.relics.keys(), 'elite')
            obj = Reward.objects.create(
                card = cards,
                relic = relic,
                gold = gold,
                game = game,
                id = game.id)
            return Response(status= 200)
        return Response(status = 400)