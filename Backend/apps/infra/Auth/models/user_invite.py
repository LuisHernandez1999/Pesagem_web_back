import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta

class UserInvite(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    email = models.EmailField()
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def is_valid(self):
        return not self.used and timezone.now() < self.expires_at

    @classmethod
    def create(cls, email: str):
        return cls.objects.create(
            email=email,
            expires_at=timezone.now() + timedelta(hours=24),
        )
