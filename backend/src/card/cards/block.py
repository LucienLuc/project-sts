from ..card import Card

class Block(Card):
    name = 'Block'
    description = 'Gain 6 block'
    mana = 1

    def on_play(self, data):
        data['battle_state']['block'] = data['battle_state']['block']+6

