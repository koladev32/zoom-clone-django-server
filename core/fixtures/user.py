from core.user.models import User
from django.contrib.auth.hashers import make_password

data_user = {
    "username": "",
    "is_active": True,
    "is_superuser": False,
    "password": make_password("12345")
}

User.objects.create_user(**data_user)