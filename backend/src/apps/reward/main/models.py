from django.db import models
from src.apps.game.main.models import Game

class Reward(models.Model):
    game = models.OneToOneField(Game, on_delete = models.CASCADE)
    card = models.JSONField(default = list, null = True)
    relic = models.JSONField(default = list, null = True)
    gold = models.IntegerField(null = True)
    
    def __str__(self):
        return str(self.id)