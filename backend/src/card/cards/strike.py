from ..card import Card

class Strike(Card):
    name = 'Strike'
    description = 'Deal 6 damage to an enemy'
    mana = 1

    def on_play(self):
        print("I attack")

