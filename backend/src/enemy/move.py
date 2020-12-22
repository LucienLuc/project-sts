class Move():
    def __init__(self, move_type, count, value):
        #valid MOVE_TYPE's
        # attack
        # block 
        self.type = move_type
        self.count = count
        self.value = value