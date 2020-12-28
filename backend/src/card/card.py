import abc
from abc import ABC, abstractmethod
import json

class Card(ABC):
    #str
    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    #str
    @property
    @abstractmethod
    def description(self):
        raise NotImplementedError

    #int
    @property
    @abstractmethod
    def mana(self):
        raise NotImplementedError

    # dict
    # Define tags as a key: value pair where key is the name of the tag
    # Available tags:
    # exhaust - card does not get put into discard pile after play
    @property
    @abstractmethod
    def tags(self):
        raise NotImplementedError
    
    #Let return value be the number of cards to draw after card play
    @abstractmethod
    def on_play(self, data):
        raise NotImplementedError

    def attack_modifier(self, base, status_effects, enemy_effects):
        strength_value = 0
        weak_multiplier = 1
        vulnerable_multiplier = 1
        try:
            strength_value = status_effects['strength']
        except(KeyError):
            pass

        try:
            status_effects['weak']
            weak_multiplier = 0.75
        except(KeyError):
            pass
        
        try:
            enemy_effects['vulnerable']
            vulnerable_multiplier = 1.5
        except(KeyError):
            pass
        return int((base + strength_value) * weak_multiplier * vulnerable_multiplier)

    def block_modifier(self, base, status_effects):
        fortify_value = 0
        fragile_multiplier = 1
        try:
            fortify_value = status_effects['fortify']
        except(KeyError):
            pass

        try:
            status_effects['fragile']
            fragile_multiplier = 0.75
        except(KeyError):
            pass
        return int(base + fortify_value * fragile_multiplier)

class CardEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return {
                "name": obj.name,
                "description": obj.description,
                "mana": obj.mana,
                "tags": obj.tags
                }
        except:
            return json.JSONEncoder.default(self, obj)