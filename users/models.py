from django.contrib.auth.models import AbstractBaseUser, Group, Permission, PermissionsMixin
from django.contrib.auth.models import BaseUserManager as BUM  # noqa: N817
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel


class UserManager(BUM):
    def create_user(self, email, is_active=True, is_admin=False, password=None):
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email.lower())

        user = self.model(
            email=email,
            is_active=is_active,
            is_admin=is_admin,
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
        ),
    )
    is_admin = models.BooleanField(default=False)

    # Add the groups and user_permissions fields with unique related_names
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Unique related_name
        blank=True,
        help_text=_("The groups this user belongs to."),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Unique related_name
        blank=True,
        help_text=_("Specific permissions for this user."),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    @property
    def is_staff(self):
        return self.is_admin
