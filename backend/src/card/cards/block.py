from ..card import Card

class Block(Card):
    name = 'Block'
    description = 'Block 6 damage'
    mana = 1

    def on_play(self):
        print("I block")

