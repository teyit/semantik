from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Leaving it empty for possible future updates
    def __str__(self):
        return self.username
