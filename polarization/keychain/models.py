from django.db import models
from django.utils import timezone

class Key(models.Model):
    consumer_key = models.CharField(max_length=150)
    consumer_key_secret = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    access_token_secret = models.CharField(max_length=150)
    last_used = models.DateTimeField(null=True, blank=True)
    stream = models.BooleanField(default=False)

    @property
    def is_usable(self):
        return self.last_used < timezone.now() - timezone.timedelta(minutes=15)

    def __str__(self):
        return self.access_token
