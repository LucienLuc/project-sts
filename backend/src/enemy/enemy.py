import abc
from abc import ABC, abstractmethod
import json

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

class EnemyEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return {
                'enemy_name': obj.enemy_name,
                'max_health': obj.max_health,
                'curr_health': obj.curr_health,
                'field_position': obj.field_position,
                'next_move': obj.next_move
                }
        except:
            return json.JSONEncoder.default(self, obj)