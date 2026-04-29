from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
     autorizado = models.BooleanField(default=False)

     foto = models.ImageField(upload_to='fotos/', null=True, blank=True)
