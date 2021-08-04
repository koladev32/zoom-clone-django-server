from core.room.serializers import RoomSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

# TODO: Review the necessity of adding custom permission here


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    serializer_class = RoomSerializer
    permission_classes = (AllowAny,)