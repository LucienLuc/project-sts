from rest_framework import viewsets

# importing serializers
# from django.contrib.auth import get_user_model
# User = get_user_model()

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# importing models
from django.db.models import F
from rest_framework.response import Response
from src.apps.battle.main.models import Battle
from src.apps.battle.main.serializers import BattleSerializer
from src.apps.game.main.models import Game
from src.apps.game.main.serializers import GameSerializer
from src.apps.enemy.main.models import Enemy
from src.apps.enemy.main.serializers import EnemySerializer

from src.card.cards import *
from src.card.card import Card, CardEncoder
from src.enemy.enemy import Enemy as ClassEnemy
from src.enemy.enemy import EnemyEncoder
from src.enemy.enemies import *

from django.shortcuts import get_object_or_404
import json
import random

#TODO
def determine_enemies(step):
    res = ['slime','rat']
    # no more than 4 enemies per battle
    # maybe don't crash the program if this fails
    assert(len(res) <= 4)
    return res

# hand, deck, discard - list of dicts (Card)
# amount - number of cards to draw
# mutates hand, deck, discard
def draw_cards(hand, deck, discard, amount):
    for i in range(amount):
        try:
            hand.append(deck[0])
            deck.pop(0)
        # Ran out of cards in deck, put all cards from discard into deck and continue drawing cards
        except(IndexError):
            deck = discard
            discard = []
            # if run out of cards to draw after putting discard, stop drawing cards
            try:
                hand.append(deck[0])
                deck.pop(0)
            except(IndexError):
                break
    return

class BattleViewSet(viewsets.ModelViewSet):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer

    # @action(detail=True, methods=['post', 'get'])
    # def foo(self, request, pk):
    #     return Response(status= 200)

    @action(detail=True, methods=['post'])
    def play_card(self, request, pk):
        battle = self.get_object()
        # check if target is a valid int
        try:
            target = int(request.data['target'])
        except:
            return Response(status=404)
        
        # check if target is a valid target
        if(len(battle.enemy_set.all()) < target):
            return Response(status=404)

        #Get card class
        try:
            card_name = request.data['card_name']
            card_module = globals()[card_name.lower()]
            card = getattr(card_module, card_name)
        except:
            return Response(status=404)

        # check if enough curr_mana
        if battle.curr_mana < card.mana:
            return Response(status=409)
        battle.curr_mana = battle.curr_mana - card.mana

        #verify card is in battle.hand by trying to remove from battle.hand and add to discard
        try:
            card_json = json.dumps(card, cls=CardEncoder)
            battle.hand.remove(card_json)
            battle.discard.append(card_json)
        except:
            return Response(status=404)

        # Prepare data to send to card on_play() method
        enemies = battle.enemy_set.all()
        enemy_list = []
        for enemy in battle.enemy_set.all():
            enemy_list.append(json.dumps(enemy, cls=EnemyEncoder))

        data = {
            'battle_state' : {
                'curr_health': battle.curr_health,
                'max_health': battle.max_health,
                'curr_mana': battle.curr_mana,
                'max_mana': battle.max_mana,
                'deck': battle.deck,
                'hand': battle.hand,
                'discard': battle.discard,
                'enemies': enemy_list
            },
            'action' : {
                'target': int(request.data['target']),
                'card': request.data['card_name']
            }
        }
        card.on_play(self, data)
        # print(data['battle_state']['enemies'][target-1])

        # Update all fields
        battle.curr_health = data['battle_state']['curr_health']

        # how does this handle multiple targets?
        enemy_target = battle.enemy_set.get(field_position__exact = target)
        if (data['battle_state']['enemies'][target-1]['curr_health'] <= 0):
            enemy_target.delete()
        else:
            enemy_target.curr_health = data['battle_state']['enemies'][target-1]['curr_health']
            enemy_target.save()
        
        # print(battle.enemy_set.all()[1].curr_health)
        battle.save()
        return Response(status=200)

    @action(detail=True, methods=['post'])
    def end_turn(self, request, pk):
        # do all enemy's moves
        # set curr_mana = max_mana
        # put all hand into graveyard
        # get next hand
        return Response(status=200)

    @action(detail=True, methods=['get'])
    def get_state(self, request, pk):
        battle = self.get_object()
        enemy_list = []
        for enemy in battle.enemy_set.all():
            enemy_list.append(json.dumps(enemy, cls=EnemyEncoder))
        data = {
                'curr_health': battle.curr_health,
                'max_health': battle.max_health,
                'curr_mana': battle.curr_mana,
                'max_mana': battle.max_mana,
                'deck': battle.deck,
                'hand': battle.hand,
                'discard': battle.discard,
                'enemies': enemy_list
        }
        return Response(data = data, status=200)

    def create(self, request, *args, **kwargs):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            game = get_object_or_404(Game, id=serializer.validated_data['id'])
            battle = Battle.objects.create(
                curr_health = game.curr_health,
                max_health = game.max_health,
                curr_mana = game.max_mana,
                max_mana = game.max_mana,
                game = game,
                deck = game.deck, # does this make a copy or reference same thing?
                id = game.id
            )
            random.shuffle(battle.deck)
            # generate enemies
            # determined by how far one is in the game map?
            # pass params for elite and boss enemies
            # for now just create one slime and one rat
            enemy_list = determine_enemies(1)
            i = 1
            for enemy_name in enemy_list:
                enemy_module = globals()[enemy_name]
                #capitlaize because class name is capital first letter
                enemy = getattr(enemy_module, enemy_name.capitalize())
                next_move = enemy.get_next_move(self)
                Enemy.objects.create(
                    max_health = enemy.max_health,
                    curr_health = enemy.max_health,
                    enemy_name = enemy.name,
                    field_position = i,
                    battle = battle,
                    next_move = next_move
                )
                i += 1
            # hand = battle.hand
            # deck = battle.deck
            # discard = battle.discard
            # print(hand)
            draw_cards(battle.hand, battle.deck, battle.discard, 5)
            # print(hand)
            # battle.hand = hand
            # battle.deck = deck
            # battle.discard = discard
            battle.save()
            return Response(status=201)
        return Response(status=404)

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create', 'list', 'retrieve', 'end_turn', 'play_card']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]