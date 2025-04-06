from .Abstract import State
import pygame
from typing import Optional, Dict

WIDTH, HEIGHT = 1280, 720

class StateMachine:
    def __init__(self, character: "Character"):
        self.character = character
        self.current_state: Optional[State] = None #IdleState, RunState
        self.current_state_name: str = "idle"
        self.previous_state: Optional[State] = None
        self.state_enter_time: float = 0.0
        self.states: Dict[str, State] = {} # we do not know how many states we will add
        #self states can be: "idle": IdleState
    def add_state(self, state_name: str, state_class: State):
        self.states[state_name] = state_class
    
    def change_state(self, new_state_name):
        if self.current_state:
             self.current_state.exit()
             self.previous_state = self.current_state
        
        self.current_state = self.states[new_state_name]
        self.current_state_name = new_state_name
        self.current_state.enter()
        self.state_enter_time = pygame.time.get_ticks()
    
    def update(self):
        if self.current_state:
            self.current_state.update()