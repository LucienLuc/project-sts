from ..enemy import Enemy
from..move import Move
import random

class Slime(Enemy):
    name = 'Slime'
    max_health = 20

    def get_next_move(self):
        value = random.randint(0,2)
        if value == 0:
            return Move('block', 1, 6)
        else:
            return Move('attack', 1, 7)