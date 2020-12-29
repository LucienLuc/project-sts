from django.db import models
from src.apps.game.main.models import Game

class Shop(models.Model):
    game = models.OneToOneField(Game, on_delete = models.CASCADE)
    #id is same as game.id
    # 3 cards
    card1 = models.JSONField(default = dict, null = True)
    card2 = models.JSONField(default = dict, null = True)
    card3 = models.JSONField(default = dict, null = True)

    card1_cost = models.IntegerField()
    card2_cost = models.IntegerField()
    card3_cost = models.IntegerField()
    # 3 relics
    relic1 = models.JSONField(default = dict, null = True)
    relic2 = models.JSONField(default = dict, null = True)
    relic3 = models.JSONField(default = dict, null = True)

    relic1_cost = models.IntegerField()
    relic2_cost = models.IntegerField()
    relic3_cost = models.IntegerField()
    # 3 potions
    def __str__(self):
        return str(self.id)