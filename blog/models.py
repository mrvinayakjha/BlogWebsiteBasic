from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    cont = models.TextField()