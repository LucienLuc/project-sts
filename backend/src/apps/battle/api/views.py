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
from src.apps.battle.main.serializers import BattleSerializer, PlayCardSerializer
from src.apps.game.main.models import Game
from src.apps.game.main.serializers import GameSerializer
from src.apps.enemy.main.models import Enemy
from src.apps.enemy.main.serializers import EnemySerializer


from src.card.cards import *
from src.card.card import Card, CardEncoder
from src.enemy.enemy import Enemy as ClassEnemy
from src.enemy.enemy import EnemyEncoder
from src.enemy.enemies import *
from src.enemy.move import MoveEncoder

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
        # Ran out of cards in deck, put all cards from discard into deck, shuffle deck, and continue drawing cards
        except(IndexError):
            deck = discard
            random.shuffle(deck)
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

    @action(detail=True, methods=['post'])
    def play_card(self, request, pk):
        battle = self.get_object()
        serializer = PlayCardSerializer(data = request.data)
        if serializer.is_valid():
            target = serializer.validated_data['target']
            # check if target is a valid target
            if(len(battle.enemy_set.all()) < target):
                return Response(status=404)
                
            #Get card class
            try:
                card_name = serializer.validated_data['card_name'].replace(' ', '')
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
                # Only add card to discard if card's tag doesn't have exhaust
                try:
                    exhaust_value = card.tags['exhaust']
                except(KeyError):
                    battle.discard.append(card_json)
            except:
                return Response(status=404)
                
            # Prepare data to send to card on_play() method
            enemies = battle.enemy_set.all()

            data = {
                'battle': battle,
                'enemies': enemies,
                'target': serializer.validated_data['target'],
                'card': serializer.validated_data['card_name']
            }

            draw_amount = card.on_play(self, data)
            draw_cards(battle.hand, battle.deck, battle.discard, draw_amount)
            delete_enemies = enemies.filter(curr_health__lte = 0)
            for enemy in delete_enemies:
                enemy.delete()
            battle.save()
            return Response(status=200)
        return Response(status=400)

    @action(detail=True, methods=['post'])
    def end_turn(self, request, pk):
        battle = self.get_object()

        # put all hand into discard
        battle.discard.extend(battle.hand)
        battle.hand.clear()

        # do all enemy's moves
        for enemy in battle.enemy_set.all():
            move_type = enemy.next_move['type']
            # move = json.dumps(enemy['next_move'], cls = MoveEncoder)
            if (move_type == 'attack'):
                #Support for hit amount debuffs/buffs/relic interactions
                for i in range(enemy.next_move['count']):
                    player_block = battle.block - enemy.next_move['value']
                    if (player_block < 0):
                        battle.curr_health = battle.curr_health + player_block
                        battle.block = 0
                    else:
                        battle.block = player_block
            elif(move_type == 'block'):
                enemy.block = F('block') + enemy.next_move['value'] #Check this
            else:
                return Response(status = 409)

            #end of turn status effects (regen, bleed)
            try:
                regen_value = enemy.status_effects['regen']
                if regen_value == 1:
                    enemy.status_effects.pop('regen')
                else:
                    enemy.status_effects['regen'] = regen_value - 1
                enemy.curr_health += regen_value
                if(enemy.curr_health > enemy.max_health):
                    enemy.curr_health = enemy.max_health
            except(KeyError):
                pass
            try:
                bleed_value = enemy.status_effects['bleed']
                if bleed_value == 1:
                    enemy.status_effects.pop('bleed')
                else:
                    enemy.status_effects['bleed'] = enemy.status_effects['bleed'] - 1
                enemy.curr_health -= bleed_value
                enemy.save()
            except(KeyError):
                pass
            
            #deplete duration status effects (vulnerable, weak)
            try:
                value = enemy.status_effects['vulnerable']
                if value == 1:
                    enemy.status_effects.pop('vulnerable')
                else:
                    enemy.status_effects['vulnerable'] = value - 1
            except(KeyError):
                pass
            try:
                value = enemy.status_effects['weak']
                if value == 1:
                    enemy.status_effects.pop('weak')
                else:
                    enemy.status_effects['weak'] = value - 1
            except(KeyError):
                pass
                
            #check deaths
            if enemy.curr_health <= 0:
                enemy.delete()
            else:
                #get new enemies moves
                # print(enemy.name)
                enemy_module = globals()[enemy.name.lower()]
                # capitlaize because class name is capital first letter
                enemy_class = getattr(enemy_module, enemy.name.capitalize())
                next_move = enemy_class.get_next_move(self)
                enemy.next_move = next_move
                enemy.save()
            
        # Player status effects
        try:
            regen_value = battle.status_effects['regen']
            if regen_value == 1:
                battle.status_effects.pop('regen')
            else:
                battle.status_effects['regen'] = regen_value - 1
            battle.curr_health += regen_value
            if(battle.curr_health > battle.max_health):
                battle.curr_health = battle.max_health
        except(KeyError):
            pass
        try:
            bleed_value = battle.status_effects['bleed']
            if bleed_value == 1:
                battle.status_effects.pop('bleed')
            else:
                battle.status_effects['bleed'] = battle.status_effects['bleed'] - 1
            enemy.curr_health -= bleed_value
        except(KeyError):
            pass
        
        try:
            value = battle.status_effects['vulnerable']
            if value == 1:
                battle.status_effects.pop('vulnerable')
            else:
                battle.status_effects['vulnerable'] = value - 1
        except(KeyError):
            pass

        try:
            value = battle.status_effects['weak']
            if value == 1:
                battle.status_effects.pop('weak')
            else:
                battle.status_effects['weak'] = value - 1
        except(KeyError):
            pass

        battle.currmana = battle.max_mana

        # get next hand
        draw_cards(battle.hand, battle.deck, battle.discard, 5)
        battle.phase += 1
        battle.save()
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
                'status_effects': battle.status_effects,
                'block': battle.block,
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
                block = 0,
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
                    block = 0,
                    name = enemy.name,
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
        if self.action in ['create', 'list', 'retrieve', 'end_turn', 'play_card','get_state']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]