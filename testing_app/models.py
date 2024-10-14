# models.py
from django.db import models
from mongoengine import *

class RegisterData(models.Model):
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField(unique=True)
    user_password = models.CharField(max_length=255)

    def __str__(self):
        return self.user_name