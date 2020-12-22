import abc
from abc import ABC, abstractmethod

class Enemy(ABC):
    #str
    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    #int
    @property
    @abstractmethod
    def max_health(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_next_move(self):
        raise NotImplementedError
