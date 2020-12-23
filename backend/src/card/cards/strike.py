from ..card import Card
from src.enemy.enemy import EnemyEncoder
import json

class Strike(Card):
    name = 'Strike'
    description = 'Deal 6 damage to an enemy'
    mana = 1

    def on_play(self, data):
        #Do damage to target
        target = data['action']['target']
        enemy_json = json.loads(data['battle_state']['enemies'][target-1])
        enemy_json['curr_health'] = enemy_json['curr_health']-6
        data['battle_state']['enemies'][target-1] = enemy_json