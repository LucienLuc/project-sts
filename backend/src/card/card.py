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

    @abstractmethod
    def on_play(self, data):
        raise NotImplementedError

class CardEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return {
                "name": obj.name,
                "description": obj.description,
                "mana": obj.mana
                }
        except:
            return json.JSONEncoder.default(self, obj)