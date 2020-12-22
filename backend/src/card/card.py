import abc
from abc import ABC, abstractmethod

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
    def on_play(self):
        raise NotImplementedError
