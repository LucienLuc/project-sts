from ..card import Card
import json

class DeepCut(Card):
    name = 'Deep Cut'
    description = 'Deal 4 damage and inflict 2 Bleed'
    mana = 1

    def on_play(self, data):
        target = data['action']['target']
        enemy_json = json.loads(data['battle_state']['enemies'][target-1])

        new_attack = Card.attack_modifier(self, 4, data['battle_state']['status_effects'], data['battle_state']['status_effects'])
        enemy_json['curr_health'] = enemy_json['curr_health'] - new_attack
        
        try:
            value = enemy_json['status_effects']['bleed']
            enemy_json['status_effects'].update({'bleed': value + 2})
        except(KeyError):
             enemy_json['status_effects'].update({'bleed': 2})

        data['battle_state']['enemies'][target-1] = enemy_json

