from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from src.apps.battle.main.models import Battle

class Enemy(models.Model):
    max_health = models.IntegerField()
    curr_health = models.IntegerField()
    block = models.IntegerField()
    ENEMYNAME = (
        ('rat','Rat'),
        ('slime', 'Slime'),
    )
    name = models.CharField(max_length = 7, choices = ENEMYNAME)
    battle = models.ForeignKey(Battle, on_delete = models.CASCADE)
    field_position = models.IntegerField(validators = [MaxValueValidator(4), MinValueValidator(1)])
    #Stores move object
    next_move = models.JSONField(default = dict)
    
    def __str__(self):
        return str(self.id)