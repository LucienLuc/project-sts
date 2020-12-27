from ..card import Card
import json

class Shatter(Card):
    name = 'Shatter'
    description = 'Deal 4 damage and inflict 2 Vulnerable'
    mana = 2
    tags = {}

    def on_play(self, data):
        target = data['action']['target']
        enemy_json = json.loads(data['battle_state']['enemies'][target-1])

        new_attack = Card.attack_modifier(self, 4, data['battle_state']['status_effects'], data['battle_state']['status_effects'])
        enemy_json['curr_health'] = enemy_json['curr_health'] - new_attack
        
        try:
            value = enemy_json['status_effects']['vulnerable']
            enemy_json['status_effects'].update({'vulnerable': value + 2})
        except(KeyError):
             enemy_json['status_effects'].update({'vulnerable': 2})

        data['battle_state']['enemies'][target-1] = enemy_json
        return 0
