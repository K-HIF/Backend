from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class MedicappUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class MedicappUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MedicappUserManager()

    def _str_(self):
        return self.email

    class Meta:
        db_table = 'medicapp_user'


class StarCount_2(models.Model):
    count = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return str(self.count)


class DownvoteCounter(models.Model):
    count = models.PositiveIntegerField(default=0)

    def _str_(self):
        return f"Total Downvotes: {self.count}"


class UserDownvote(models.Model):
    user = models.OneToOneField(MedicappUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} downvoted at {self.timestamp}"


class IPDownvote(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.ip_address} downvoted at {self.timestamp}"