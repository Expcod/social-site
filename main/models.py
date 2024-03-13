from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Custom fields if needed
    age = models.PositiveIntegerField(null=True, blank=True)
    f_name = models.CharField(max_length=255)
    # Other custom fields...

class User(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    phone  = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)

class Chat(models.Model):
    ...

class Post(models.Model):
    ...

class Comment(models.Model):
    ...
class Wish(models.Model):
    ...
    
