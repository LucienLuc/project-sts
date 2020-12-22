from django.db import models

class Enemy(models.Model):
    max_health = models.IntegerField()
    curr_health = models.IntegerField()
    ENEMYTYPE = (
        ('rat','rat'),
        ('slime', 'slime'),
    )
    enemy_type = models.CharField(max_length = 7, choices = ENEMYTYPE)
    # next_move

    
    def __str__(self):
        return str(self.number)