from ..enemy import Enemy
from..move import Move
import random

class Slime(Enemy):
    name = 'Slime'
    max_health = 20

    def get_next_move(self):
        value = random.randint(0,2)
        if value == 0:
            return {
                'type': 'block',
                'count': 1,
                'value': 6
            }
        else:
            return {
                'type': 'attack',
                'count': 1,
                'value': 7
            }