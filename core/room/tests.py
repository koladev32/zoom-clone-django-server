from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from core.room.models import Room


def _create_5_rooms():
    data_room = {"name": "room", "status": "active"}

    for i in range(5):
        Room.objects.create(**data_room)


class UserTest(APITestCase):
    base_url_room = reverse("core-api:room-list")

    data_room = {"name": "room-test"}

    def test_create_room(self):
        response = self.client.post(f"{self.base_url_room}", data=self.data_room)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_create_more_than_5_rooms(self):
        _create_5_rooms()

        response = self.client.post(f"{self.base_url_room}", data=self.data_room)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
