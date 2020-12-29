from ..card import Card

class Fear(Card):
    name = 'Fear'
    description = 'Give all enemies 2 Weak'
    mana = 1
    tags = {}
    
    def on_play(self, data):
        enemy = data['enemies'].get(field_position__exact = data['target'])
        for enemy in data['enemies']:
            try:
                fear_value = enemy.status_effects['fear']
                enemy.status_effects.update({'fear': fear_value + 2})
            except(KeyError):
                enemy.status_effects.update({'fear': 2})
            enemy.save()
        return 0