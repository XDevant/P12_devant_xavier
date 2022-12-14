from django.db import models
from django.contrib.auth.models import AbstractBaseUser,\
                                       Group,\
                                       PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        if extra_fields.get("role") != "admin":
            extra_fields.setdefault('is_staff', True)
        else:
            extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        if extra_fields.get("role") != "admin":
            raise ValueError("Superuser must have role='admin'.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        NONE = 'none'
        ADMIN = 'admin'
        SUPPORT = 'support'
        SALES = 'sales'
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    role = models.CharField(choices=Role.choices,
                            max_length=16,
                            default='none')
    is_active = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} couriel:{self.email}"

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_superuser or self.role == "admin"

    def save(self, *args, **kwargs):
        if self._state.adding:
            super().save(*args, **kwargs)
            try:
                group = Group.objects.get(name=self.role)
            except ObjectDoesNotExist:
                group = Group.objects.get(name="visitor")
            self.groups.add(group)
        else:
            super().save(*args, **kwargs)
