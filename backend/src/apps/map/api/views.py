from rest_framework import viewsets

# importing serializers
# from django.contrib.auth import get_user_model
# User = get_user_model()

from rest_framework.decorators import action

# importing models
from rest_framework.response import Response
from src.apps.map.main.models import Map
from src.apps.map.main.serializers import MapSerializer

from django.shortcuts import get_object_or_404

import random
from collections import defaultdict

def generate():
    res = defaultdict(list)
    # res = {
    #     's1': [],
    #     's2': [],
    #     's3': [],
    #     's4': []
    # }


    # 4 start points
    for i in range(4):
        res[i]

    MAX_WIDTH = 6
    MIN_WIDTH = 2
    MAX_HEIGHT = 15

    insert = 4
    previous_segment = [0,1,2,3]
    next_segment = []

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
                #left side bias
                for k in range(num):
                    if next_segment[cursor] not in res[previous_segment[j]]:
                        res[previous_segment[j]].append(next_segment[cursor])
                        res[previous_segment[j]].sort()
                    if cursor != 0:
                        cursor -= 1
        previous_segment = next_segment.copy()
        next_segment.clear()
    return res

    # for i in range(MAX_HEIGHT):
    #     new_width = random.randint(3,6)
    #     #create nodes
    #     for n in range(new_width):
    #         res[insert]
    #         next_segment.append(insert)
    #         insert += 1
    #     #draw edges
    #     min_connections = min(len(previous_segment), len(next_segment))
    #     for j in range(len(previous_segment)):
    #         res[previous_segment[j]].append()
    #         num_connections = random.randint(1,3)

    # for i in range(MAX_HEIGHT):
    #     bias = random.randint(0,1)
    #     #left bias
    #     if bias == 0:
    #         for j in range(len(previous_segment)):
    #             num = random.randint(0,1)
    #             # split
    #             if len(next_segment) < MAX_WIDTH and num == 0:
    #                 attach = []
    #                 # create two nodes
    #                 res[insert]
    #                 next_segment.append(insert)
    #                 attach.append(insert)
    #                 insert+=1
    #                 res[insert]
    #                 next_segment.append(insert)
    #                 attach.append(insert)
    #                 insert+=1
    #                 for item in attach:
    #                     res[previous_segment[j]].append(item)
    #             elif len(next_segment) < MAX_WIDTH and num ==1:
    #                 pass
    #     #right bias
    #     else:
    #         pass
    return res

class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer

    # @action(detail=True, methods=['post', 'get'])
    # def foo(self, request, pk):
    #     return Response(status= 200)

    def create(self, request, *args, **kwargs):
        test_map = generate()
        print(test_map)
        return Response(status= 201)
