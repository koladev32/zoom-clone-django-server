from django.db import models
from core.abstract.models import AbstractModel, AbstractManager


class RoomManager(AbstractManager):
    pass


class Room(AbstractModel):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=(('active', 'active'), ('inactive', 'inactive')))

    objects = RoomManager()
