from django.db import models
# from ....card import card

from django.contrib.auth import get_user_model
User = get_user_model()

class Game(models.Model):

    # Each game is mapped to one user
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    GAMESTATE = (
        ('battle','battle'),
        ('shop', 'shop'),
        ('event', 'event'),
        ('map', 'map'),
        ('reward','reward')
    )
    gamestate = models.CharField(max_length = 7, choices = GAMESTATE)
    curr_health = models.IntegerField()
    max_health = models.IntegerField()
    max_mana = models.IntegerField()
    gold = models.IntegerField()
    # array of card
    deck = models.JSONField(default = list)
    relics = models.JSONField(default = dict)

    # game.id is always == user.id
    def __str__(self):
        return str(self.id)