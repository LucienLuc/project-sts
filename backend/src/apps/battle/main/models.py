from django.db import models

class Battle(models.Model):
    phase = models.IntegerField(default = 1)
    curr_health = models.IntegerField()
    max_healh = models.IntegerField()
    # enemies
    hand = []
    discard = []
    deck = []

    def __str__(self):
        return str(self.id)