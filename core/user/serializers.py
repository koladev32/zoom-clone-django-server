from rest_framework import serializers

from core.user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['public_id', 'username', 'is_active',
                  'created', 'updated']