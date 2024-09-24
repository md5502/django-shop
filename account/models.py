from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, is_active=True, is_admin=False):
        if not username:
            raise ValueError("The user must have a username")
        if not email:
            raise ValueError("The user must have an email")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_active=is_active,
            is_admin=is_admin,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            is_active=True,
            is_admin=True,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(max_length=120, unique=True)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=120, null=True, default="", blank=True)
    last_name = models.CharField(max_length=120, null=True, default="", blank=True)
    profile_img = models.ImageField(upload_to="media", default="user_profile.png")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


    def is_staff(self):
        return self.is_admin
