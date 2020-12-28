from ..card import Card
import json

class Shatter(Card):
    name = 'Shatter'
    description = 'Deal 4 damage and inflict 2 Vulnerable'
    mana = 2
    tags = {}

    def on_play(self, data):
        enemy = data['enemies'].get(field_position__exact = data['target'])
        new_attack = Card.attack_modifier(self, 4, data['battle'].status_effects, enemy.status_effects)
        enemy.curr_health -= new_attack
        try:
            value = enemy.status_effects['vulnerable']
            enemy.status_effects.update({'vulnerable': value + 2})
        except(KeyError):
             enemy.status_effects.update({'vulnerable': 2})
        enemy.save()
        return 0