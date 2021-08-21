from rest_framework import viewsets

from core.room.serializers import RoomSerializer
from core.authentication.permissions import UserPermission


class RoomViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    serializer_class = RoomSerializer
    permission_classes = (UserPermission,)
