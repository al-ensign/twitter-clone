from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = "user"
        MODERATOR = "moderator"
        ADMIN = "admin"

    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices, default=Roles.USER)
    is_blocked = models.BooleanField(default=False)
