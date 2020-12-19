from rest_framework import viewsets

# importing serializers
# from django.contrib.auth import get_user_model
# User = get_user_model()

from rest_framework.decorators import action

# importing models
from rest_framework.response import Response
from src.apps.test.main.models import Test
from src.apps.test.main.serializers import TestSerializer

from django.shortcuts import get_object_or_404
# lobbies can only be read 

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    # @action(detail=True, methods=['post', 'get'])
    # def foo(self, request, pk):
    #     return Response(status= 200)

    def create(self, request, *args, **kwargs):
        print(request.data)
        obj = Test.objects.create(number = request.data['number'])
        return Response(status= 200)
