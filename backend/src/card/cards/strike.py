from ..card import Card
from src.enemy.enemy import EnemyEncoder
import json

class Strike(Card):
    name = 'Strike'
    description = 'Deal 6 damage to an enemy'
    mana = 1
    tags = {}
    
    def on_play(self, data):
        #Do damage to target
        target = data['action']['target']
        enemy_json = json.loads(data['battle_state']['enemies'][target-1])

        new_attack = Card.attack_modifier(self, 6, data['battle_state']['status_effects'], enemy_json['status_effects'])
        enemy_json['curr_health'] = enemy_json['curr_health']-new_attack
        data['battle_state']['enemies'][target-1] = enemy_json
        return 0