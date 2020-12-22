import abc
from abc import ABC, abstractmethod, abst

class Battle(ABC):
    #int
    @property
    @abstractmethod
    def health(self):
        raise NotImplementedError

    #arr
    @property
    @abstractmethod
    def hand(self):
        raise NotImplementedError

    #arr
    @property
    @abstractmethod
    def graveyard(self):
        raise NotImplementedError

    #arr
    @property
    @abstractmethod
    def discard(self):
        raise NotImplementedError

    #arr
    @property
    @abstractmethod
    def enemies(self):
        raise NotImplementedError
