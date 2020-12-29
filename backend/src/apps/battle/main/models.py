from django.db import models

from src.apps.game.main.models import Game

class Battle(models.Model):
    phase = models.IntegerField(default = 1)
    curr_health = models.IntegerField()
    max_health = models.IntegerField()
    curr_mana = models.IntegerField()
    max_mana = models.IntegerField()
    block = models.IntegerField()
    status_effects = models.JSONField(default = dict)
    game = models.OneToOneField(Game, on_delete = models.CASCADE)

    # enemies foreign key field
    hand = models.JSONField(default = list)
    discard = models.JSONField(default = list)
    deck = models.JSONField(default = list)
    relics = models.JSONField(default = dict)
    #id is same as game.id
    def __str__(self):
        return str(self.id)
        # return {
        #     'phase': self.phase,
        #     'curr_health': self.curr_health
        #     # max_health = models.IntegerField()
        #     # curr_mana = models.IntegerField()
        #     # max_mana = models.IntegerField()
        #     # game = models.OneToOneField(Game, on_delete = models.CASCADE)

        #     # # enemies
        #     # hand = models.JSONField(default = list)
        #     # discard = models.JSONField(default = list)
        #     # deck = models.JSONField(default = list)
        # }