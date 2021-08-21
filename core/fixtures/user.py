from core.user.models import User

data_user = {
    "username": "",
    "is_active": True,
    "is_superuser": False
}

User.objects.create_user(**data_user)