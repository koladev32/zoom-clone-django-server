from rest_framework import serializers

from core.room.models import Room


# TODO: Add the moderator id

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['public_id, name, created, updated']
