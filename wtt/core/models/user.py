import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True, verbose_name=_("UUID"))

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"User {self.id}"
