from django.db import models

from src.apps.battle.main.models import Battle

class Enemy(models.Model):
    max_health = models.IntegerField()
    curr_health = models.IntegerField()
    ENEMYTYPE = (
        ('rat','rat'),
        ('slime', 'slime'),
    )
    enemy_type = models.CharField(max_length = 7, choices = ENEMYTYPE)
    battle = models.ForeignKey(Battle, on_delete = models.CASCADE)
    #Stores move object
    next_move = {}
    
    def __str__(self):
        return str(self.number)