from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

# class UserProfile(models.Model):
#     id = models.AutoField(primary_key=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)
#     dob = models.DateField()
#     USER_ROLE_CHOICES = [
#         ('user', 'User'),
#         ('admin', 'Admin'),
#     ]
#     role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES)
    