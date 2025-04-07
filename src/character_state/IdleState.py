from .Abstract import State

class IdleState(State):
    def __init__(self, character):
        super().__init__(character)
        
    def enter(self):
        self.character.state = "idle"
        