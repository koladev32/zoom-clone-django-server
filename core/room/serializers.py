from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.room.models import Room


class RoomSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')
    name = serializers.CharField(max_length=35, min_length=5, required=True)

    def validate(self, attrs):

        rooms_count = Room.objects.filter(status='active').count()

        if rooms_count + 1 > 5:
            raise ValidationError({'room': "There is more than 5 rooms. Wait a moment."})

        return attrs

    def create(self, validated_data):
        validated_data['status'] = 'active'
        room = Room.objects.create(**validated_data)
        return room

    class Meta:
        model = Room
        fields = ['id', 'name', 'created', 'updated', 'status']
        read_only_fields = ['public_id', 'status']
