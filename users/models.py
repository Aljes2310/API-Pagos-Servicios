from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    email=models.CharField(max_length=200 , unique=True,)
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    
    #con cual campo identificas usuarios, esto aparece en el admin
    USERNAME_FIELD = 'email'
    """ Campos requeridos al crear el superusuario """
    REQUIRED_FIELDS = ['username',"password"]

    def __str__(self):
        return self.email

    class Meta:
        db_table="users"

from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario necesita que is_staff sea verdadero")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario necesita que is_superuser sea verdadero")

        return self.create_user(email=email, password=password, **extra_fields)