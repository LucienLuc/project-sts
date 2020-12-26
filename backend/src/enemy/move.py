import json

class Move():
    def __init__(self, move_type, count, value):
        #valid MOVE_TYPE's
        # attack
        # block 
        self.type = move_type
        self.count = count
        self.value = value

class MoveEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return {
                'type': obj.type,
                'count': obj.count,
                'value': obj.value,
                }
        except:
            return json.JSONEncoder.default(self, obj)