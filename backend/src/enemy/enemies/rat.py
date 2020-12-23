from ..enemy import Enemy
from..move import Move
import random

class Rat(Enemy):
    name = 'Rat'
    max_health = 15

    def get_next_move(self):
        return {
                'type': 'attack',
                'count': 1,
                'value': 5
            }