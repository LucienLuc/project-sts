from rest_framework import viewsets

# importing serializers
# from django.contrib.auth import get_user_model
# User = get_user_model()

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

# importing models
from rest_framework.response import Response
from src.apps.battle.main.models import Battle
from src.apps.battle.main.serializers import BattleSerializer
from src.apps.game.main.models import Game
from src.apps.game.main.serializers import GameSerializer

from django.shortcuts import get_object_or_404


class BattleViewSet(viewsets.ModelViewSet):
    queryset = Battle.objects.all()
    serializer_class = BattleSerializer

    # @action(detail=True, methods=['post', 'get'])
    # def foo(self, request, pk):
    #     return Response(status= 200)

    @action(detail=True, methods=['post'])
    def play_card(self, request, pk):
        battle = self.get_object()
        print(battle.deck)
        return Response(status=200)

    @action(detail=True, methods=['post'])
    def end_turn(self, request, pk):
        # do all enemy's moves
        # set curr_mana = max_mana
        # put all hand into graveyard
        # get next hand
        return Response(status=200)

    def create(self, request, *args, **kwargs):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            game = get_object_or_404(Game, id=serializer.validated_data['id'])
            obj = Battle.objects.create(
                curr_health = game.curr_health,
                max_health = game.max_health,
                curr_mana = game.max_mana,
                max_mana = game.max_mana,
                game = game,
                id = game.id
            )
            #does this copy or reference the same deck in memory?
            print(game.deck)
            obj.deck.append(game.deck)
            # print(obj.deck)
            return Response(status=201)
        return Response(status=404)

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create', 'list', 'retrieve', 'end_turn', 'play_card']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]