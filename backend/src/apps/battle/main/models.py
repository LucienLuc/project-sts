from django.db import models

from src.apps.game.main.models import Game

class Battle(models.Model):
    phase = models.IntegerField(default = 1)
    curr_health = models.IntegerField()
    max_health = models.IntegerField()
    curr_mana = models.IntegerField()
    max_mana = models.IntegerField()
    game = models.OneToOneField(Game, on_delete = models.CASCADE)

    # enemies
    hand = []
    discard = []
    deck = []

    #id is same as game.id
    def __str__(self):
        return str(self.id)