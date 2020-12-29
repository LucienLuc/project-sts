COMMON_RELIC_POOL = [
    'steroids', 'calcium supplements', 'ember', 'mango'
]
UNCOMMON_RELIC_POOL = [
    'vacuum', 'jack in the box', 'pineapple'
]
RARE_RELIC_POOL = [
    'onion', 'mobius strip', 'ancient coin', 'watermelon', 'battery', 'armadillo shell'
]

SHOP_RELIC_POOL = [
    'membership card'
]
BOSS_RELIC_POOL = [
    'philosopher\'s stone', 'toy ship', 'glass vial', 'bell', 'pandora\'s box'
]

RELIC_DICT = {
    # COMMON
    'Steroids': 'At the start of combat, gain 1 Strength.', 
    'Calcium Supplements': 'At the start of combat, gain 1 Fortify.',
    'Tome of Knowledge': 'At the start of combat, draw 2 additional cards.',
    'Ember': 'At the end of combat, restore 6 health.',
    'Mango': 'Gain 7 Max HP.',
    # UNCOMMON
    'Vacuum': 'Whenever an enemy dies, draw 1 card and gain 1 energy',
    'Jack In The Box': 'At the start of combat, all enemies gain 1 Weak',
    'Pineapple': 'Gain 10 Max HP.',

    # RARE
    'Onion': 'You can no longer become Weak.',
    'Mobius Strip': 'Whenever you have no cards in hand, draw 1 card.',
    'Ancient Coin': 'Gain 300 gold.',
    'Watermelon': 'Gain 14 Max HP.',
    'Battery': 'Energy is conserved between turns.', #
    'Armadillo Shell': 'At the start of combat, gain 4 Plated Armor.',
    #SHOP
    'Membership Card': r'50% discount on all shop purchases',

    #BOSS
    'Philosopher\'s Stone':'Gain 1 max mana. At the start of combat, all enemies gain 1 Strength.',
    'Toy Ship': 'Gain 1 max mana. You can no longer gain gold.',
    'Glass Vial': 'Gain 1 max mana. You can no longer obtain potions.',
    'Bell': 'Gain 1 max mana. You can no longer rest at campfires.',
    'Pandora\'s Box': 'Obtain a Curse and 3 relics'
}

RELIC_POOL = []
RELIC_POOL.append(COMMON_RELIC_POOL)
RELIC_POOL.append(UNCOMMON_RELIC_POOL)
RELIC_POOL.append(RARE_RELIC_POOL)
RELIC_POOL.append(SHOP_RELIC_POOL)
RELIC_POOL.append(BOSS_RELIC_POOL)

def start_of_battle_relics(data):
    cards_to_draw = 0
    try:
        data['battle'].relics['Steroids']
        data['battle'].status_effects.update({'strength': 1})
    except(KeyError):
        pass
    try:
        data['battle'].relics['Calcium Supplements']
        data['battle'].status_effects.update({'fortify': 1})
    except(KeyError):
        pass
    try:
        data['battle'].relics['Tome of Knowledge']
        cards_to_draw += 2
    except(KeyError):
        pass
    try:
        data['battle'].relics['Jack in the Box']
        for enemy in data['enemies']:
            enemy.status_effects.update({'weak': 1})
            enemy.save()
    except(KeyError):
        pass
    try:
        data['battle'].relics['Armadillo Shell']
        data['battle'].status_effects.update({'plated armor': 4})
    except(KeyError):
        pass
    try:
        data['battle'].relics['Philosopher\'s Stone']
        for enemy in data['enemies']:
            enemy.status_effects.update({'strength': 1})
            enemy.save()
    except(KeyError):
        pass
    return cards_to_draw

def start_turn_relics(data):
    return

def end_turn_relics(data):
    flag = False
    pass

def play_card_relics(data):
    flag = False
    pass

def end_of_battle_relics(data):
    flag = False
    pass