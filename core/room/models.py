from django.db import models
from core.abstract.models import AbstractModel, AbstractManager


class RoomManager(AbstractManager):
    pass


class Room(AbstractModel):
    creator = models.ForeignKey("core_user.User", on_delete=models.CASCADE, related_name='user_set')
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=(('active', 'active'), ('inactive', 'inactive')))

    objects = RoomManager()
