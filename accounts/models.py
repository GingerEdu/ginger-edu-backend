from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


# Create your models here.


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
