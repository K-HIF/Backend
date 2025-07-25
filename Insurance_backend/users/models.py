from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings  # to access the schema from .env (via settings)

class InsuranceUserManager(BaseUserManager):
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


class InsuranceUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150,unique=True)  
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = InsuranceUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'insurance_user'  



class StarCount(models.Model):
    count = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.count)
    

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    downvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title