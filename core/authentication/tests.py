from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class AuthenticationTest(APITestCase):
    base_url_login = reverse("core-api:auth-login-list")
    base_url_register = reverse("core-api:auth-register-list")
    base_url_refresh = reverse("core-api:auth-refresh-list")

    data_register = {"username": "test", "password": "password"}

    data_login = {"password": "12345678", "username": "koladev32"}

    def test_register(self):
        response = self.client.post(
            f"{self.base_url_register}", data=self.data_register
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        response = self.client.post(f"{self.base_url_login}", data=self.data_login)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh(self):
        # Login to retrieve token

        response = self.client.post(f"{self.base_url_login}", data=self.data_login)
        response_data = response.json()

        refresh = response_data["refresh"]

        data_refresh = {
            'refresh': refresh
        }

        # Refresh token

        response = self.client.post(f"{self.base_url_refresh}", data=data_refresh)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
