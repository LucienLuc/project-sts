from ..card import Card

class Block(Card):
    name = 'Block'
    description = 'Gain 6 block'
    mana = 1

    def on_play(self, data):
        new_block = Card.block_modifier(self, 6, data['battle_state']['status_effects'])
        data['battle_state']['block'] = data['battle_state']['block']+ new_block

