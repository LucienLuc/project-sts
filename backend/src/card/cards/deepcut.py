from ..card import Card
import json

class DeepCut(Card):
    name = 'Deep Cut'
    description = 'Deal 4 damage and inflict 2 Bleed'
    mana = 1
    tags = {}
    
    def on_play(self, data):
        enemy = data['enemies'].get(field_position__exact = data['target'])
        new_attack = Card.attack_modifier(self, 4, data['battle'].status_effects, enemy.status_effects)
        enemy.curr_health -= new_attack
        try:
            value = enemy.status_effects['bleed']
            enemy.status_effects.update({'bleed': value + 2})
        except(KeyError):
             enemy.status_effects.update({'bleed': 2})
        enemy.save()
        return 0
