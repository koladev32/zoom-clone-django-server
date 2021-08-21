from core.user.models import User

data_user = {
    "username": "koladev32",
    "password": "12345678"
}

User.objects.create_user(**data_user)