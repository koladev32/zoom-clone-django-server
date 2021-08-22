from django.db import models
import uuid

from django.core.exceptions import ObjectDoesNotExist, ValidationError



class AbstractManager(models.Manager):
    def get_object_by_public_id(self, public_id):
        try:
            instance = self.get(public_id=public_id)
        except (ObjectDoesNotExist, ValueError, TypeError, ValidationError):
            return None

        return instance


class AbstractModel(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = AbstractManager()

    class Meta:
        abstract = True
