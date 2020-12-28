from ..card import Card
from src.enemy.enemy import EnemyEncoder
import json

class Strike(Card):
    name = 'Strike'
    description = 'Deal 6 damage to an enemy'
    mana = 1
    tags = {}
    
    def on_play(self, data):
        enemy = data['enemies'].get(field_position__exact = data['target'])
        new_attack = Card.attack_modifier(self, 6, data['battle'].status_effects, enemy.status_effects)
        enemy.curr_health -= new_attack
        enemy.save()
        return 0