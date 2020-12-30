from django.db import models
from src.apps.game.main.models import Game

class Map(models.Model):
    game = models.OneToOneField(Game, on_delete = models.CASCADE)
    game_map = models.JSONField(default = dict)
    game_key = models.JSONField(default = dict)
    position = models.IntegerField()
    path = models.JSONField(default = list)

    def __str__(self):
        return str(self.id)