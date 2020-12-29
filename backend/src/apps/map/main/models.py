from django.db import models
from src.apps.game.main.models import Game

class Map(models.Model):
    game_map = models.JSONField(default = dict)
    game = models.OneToOneField(Game, on_delete = models.CASCADE)
    def __str__(self):
        return str(self.id)