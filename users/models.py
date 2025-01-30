from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_deleted = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['email']),        # Index for email field
            models.Index(fields=['is_deleted']),   # Index for is_deleted field
        ]

    def createsuperuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(username, email, password, **extra_fields)

    def delete(self):
        self.is_delete=True
        self.is_active=False
        self.save()
