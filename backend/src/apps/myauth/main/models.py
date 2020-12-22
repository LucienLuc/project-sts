from django.contrib.auth.models import AbstractBaseUser

from django.db import models

from src.apps.game.main.models import Game

class User(AbstractBaseUser):
   # Since there is no primary_key = True on any models, Django auto sets
   # id = models.AutoField(primary_key=True)
   # id increments by 1 each time a user is created

   username = models.CharField(max_length=30)

   #unique identifier
   USERNAME_FIELD = 'id'
