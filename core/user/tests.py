from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class UserTest(APITestCase):
    base_url_user = reverse("core-api:user-list")
    base_url_login = reverse("core-api:auth-login-list")

    data_login = {"password": "12345678", "username": "koladev32"}

    def test_retrieve_user(self):
        response = self.client.post(f"{self.base_url_login}", data=self.data_login)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()

        access = response_data["access"]
        user_public_id = response_data["user"]["public_id"]

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)

        response = self.client.get(f"{self.base_url_user}{user_public_id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
