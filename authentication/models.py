from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_owner = models.BooleanField(default=False)

    def get_full_name(self) -> str:
        return super().get_full_name()