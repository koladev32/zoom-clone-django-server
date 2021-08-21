from rest_framework.viewsets import ModelViewSet
from django.http import Http404

from core.authentication.permissions import UserPermission
from core.user.serializers import UserSerializer
from core.user.models import User


class UserViewSet(ModelViewSet):
    http_method_names = ['get']
    permission_classes = (UserPermission,)
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all().exclude(is_superuser=True)
        return Http404

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]
        if lookup_field_value == 'current':
            obj = self.request.user
        else:
            obj = User.objects.get_object_by_public_id(lookup_field_value)

        self.check_object_permissions(self.request, obj)

        return obj
