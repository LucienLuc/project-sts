from rest_framework import viewsets

# importing serializers
# from django.contrib.auth import get_user_model
# User = get_user_model()

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict

# importing models
from rest_framework.response import Response
from src.apps.map.main.models import Map
from src.apps.map.main.serializers import MapSerializer, MoveSerializer
from src.apps.game.main.models import Game
from src.apps.game.main.serializers import GameSerializer

from django.shortcuts import get_object_or_404

import random
from collections import defaultdict

def generate():
    res = defaultdict(list)
    # 4 start points
    for i in range(4):
        res[i]
    MAX_WIDTH = 6
    MIN_WIDTH = 2
    MAX_HEIGHT = 15

    insert = 4
    previous_segment = [0,1,2,3]
    next_segment = []
    segments = []

    for i in range(MAX_HEIGHT):
        if i == MAX_HEIGHT-1:
            new_width = 1
        else:
            new_width = random.randint(3,6)
        # create nodes
        for n in range(new_width):
            res[insert]
            next_segment.append(insert)
            insert += 1
        bias = random.randint(0,1)
        #draw connections
        #left side bias
        if bias == 0:
            cursor = 0
            for j in range(len(previous_segment)):
                # Create random number of connections for each node before (1-3)
                num = random.randint(1,3)
                bias = random.randint(0,1)
                for k in range(num):
                    if next_segment[cursor] not in res[previous_segment[j]]:
                        res[previous_segment[j]].append(next_segment[cursor])
                    if cursor != len(next_segment)-1:
                        cursor += 1
        #right side bias                
        else:
            cursor = new_width-1
            for j in range(len(previous_segment)-1,-1,-1):
                # Create random number of connections for each node before (1-3)
                num = random.randint(1,3)
                for k in range(num):
                    if next_segment[cursor] not in res[previous_segment[j]]:
                        res[previous_segment[j]].append(next_segment[cursor])
                        res[previous_segment[j]].sort()
                    if cursor != 0:
                        cursor -= 1
        previous_segment = next_segment.copy()
        segments.append(next_segment.copy())
        next_segment.clear()

    #Generate map key
    key = {}
    curr_level = 0
    for level in segments:
        for item in level:
            if curr_level == 0:
                key.update({item: 'battle'})
            elif curr_level == 1:
                selector = random.randint(0,1)
                if selector == 0:
                    key.update({item: 'event'})
                else:
                    key.update({item: 'battle'})
            elif curr_level >= 2 and curr_level <= 4:
                selector = random.randint(0,5)
                if selector == 0:
                    key.update({item: 'shop'})
                elif selector == 1 or selector == 2:
                    key.update({item: 'event'})
                else:
                    key.update({item: 'battle'})
            elif curr_level >= 5 and curr_level <= 7:
                selector = random.randint(0,7)
                if selector == 0:
                    key.update({item: 'battle'})
                elif selector == 1:
                    key.update({item: 'event'})
                elif selector >= 2 and selector <= 4:
                    key.update({item: 'elite'})
                else:
                    key.update({item: 'rest'})
            elif curr_level == 8:
                key.update({item: 'treasure'})
            elif curr_level >= 9 and curr_level <= 12:
                selector = random.randint(0,7)
                if selector == 0:
                    key.update({item: 'elite'})
                elif selector == 1:
                    key.update({item: 'shop'})
                elif selector == 2:
                    key.update({item: 'rest'})
                elif selector >= 3 <= 5:
                    key.update({item: 'battle'})
                else:
                    key.update({item: 'event'})
            elif curr_level == 13:
                key.update({item: 'rest'})
            elif curr_level == 14:
                key.update({item: 'boss'})
        curr_level += 1
    return dict(res), dict(key)

class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    @action(detail=True, methods=['post'])
    def move(self, request, pk):
        serializer = MoveSerializer(data=request.data)
        if serializer.is_valid():
            next_position = serializer.validated_data['next_position']
            obj = self.get_object()
            # first move
            if obj.position == -1:
                if next_position >= 0 and next_position <= 3:
                    obj.position = next_position
                    obj.path.append(next_position)
                    obj.save()
                    return Response(status= 200)
                else:
                    return Response(status = 409)
            # all other moves
            if next_position in obj.game_map[str(obj.position)]:
                obj.position = next_position
                obj.path.append(next_position)
                obj.save()
                return Response(status= 200)
            else:
                return Response(status =409)
        return Response(status=400)

    @action(detail=True, methods=['get'])
    def get_state(self, request, pk):
        obj = self.get_object()
        data = model_to_dict(obj)
        return Response(data=data, status=200)

    def create(self, request, *args, **kwargs):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            game = get_object_or_404(Game, id=serializer.validated_data['id'])
            game_map, game_key = generate()
            # print(game_map)
            obj = Map.objects.create(
                game = game,
                id = game.id,
                position = -1,
                game_map = game_map,
                game_key = game_key
            )
            return Response(status= 201)
        return Response(status = 400)

    def get_permissions(self):
        permission_classes = []
        if self.action in ['create', 'list', 'retrieve', 'move']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]