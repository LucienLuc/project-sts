from ..card import Card
from src.enemy.enemy import EnemyEncoder
import json

class Fear(Card):
    name = 'Fear'
    description = 'Give all enemies 2 Weak'
    mana = 1
    tags = {'all': 1}
    
    def on_play(self, data):
        #Do damage to target
        # target = data['action']['target']
        # enemy_json = json.loads(data['battle_state']['enemies'][target-1])
        for i in range(len(data['battle_state']['enemies'])):
            enemy_json = json.loads(data['battle_state']['enemies'][i])
            try:
                fear_value = enemy_json['status_effects']['fear']
                enemy_json['status_effects'].update({'fear': fear_value + 2})
            except(KeyError):
                enemy_json['status_effects'].update({'fear': 2})
            data['battle_state']['enemies'][i] = enemy_json
        return 0