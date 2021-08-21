from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from core.authentication.permissions import UserPermission
from core.user.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    http_method_names = ['get']
    permission_classes = (IsAuthenticated, UserPermission)
    serializer_class = UserSerializer
