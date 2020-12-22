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
        ('rewards','rewards')
    )
    gamestate = models.CharField(max_length = 7, choices = GAMESTATE)
    curr_health = models.IntegerField()
    max_health = models.IntegerField()
    gold = models.IntegerField()
    # array of card
    deck = []
    #array of relic
    relic = []

    # game.id is always == user.id
    def __str__(self):
        return str(self.id)