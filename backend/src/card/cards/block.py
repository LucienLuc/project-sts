from ..card import Card

class Block(Card):
    name = 'Block'
    description = 'Gain 6 block'
    mana = 1
    tags = {}
    
    def on_play(self, data):
        new_block = Card.block_modifier(self, 6, data['battle'].status_effects)
        data['battle'].block += new_block
        return 0
