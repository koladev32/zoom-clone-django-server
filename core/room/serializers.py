from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.room.models import Room
from core.user.models import User


class RoomSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='public_id'
    )
    name = serializers.CharField(max_length=35, min_length=5, required=True)

    def validate(self, attrs):
        creator = attrs.get('creator')

        if not creator.is_active:
            raise ValidationError({'user': 'This user can\'t host a room.'})

        try:
            Room.objects.get(creator=creator, status='active')
            raise ValidationError({'user': 'This user is hosting a room.'})
        except ObjectDoesNotExist:
            return attrs

    class Meta:
        model = Room
        fields = ['public_id', 'creator', 'name', 'created', 'updated']
        read_only_fields = ['public_id']
