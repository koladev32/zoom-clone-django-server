from django.db import models
from core.abstract.models import AbstractModel, AbstractManager


class RoomManager(AbstractManager):
    pass


class Room(AbstractModel):
    name = models.CharField(max_length=255)

    # TODO : Add moderator which will be an authenticated user user
