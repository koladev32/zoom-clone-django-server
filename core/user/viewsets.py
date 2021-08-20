from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from core.user.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    http_method_names = ('get')
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
