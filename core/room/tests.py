from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from core.user.models import User


class UserTest(APITestCase):
    base_url_room = reverse("core-api:room-list")
    base_url_login = reverse("core-api:auth-login-list")

    data_login = {"password": "12345678", "username": "koladev32"}

    data_room = {"name": "room-test"}

    def test_create_room(self):
        response = self.client.post(f"{self.base_url_login}", data=self.data_login)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        access = response_data["access"]
        user_public_id = response_data["user"]["public_id"]

        self.data_room['creator'] = user_public_id

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)

        response = self.client.post(f"{self.base_url_room}", data=self.data_room)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
