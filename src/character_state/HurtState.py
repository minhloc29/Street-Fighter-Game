from .Abstract import State
import pygame

class HurtState(State):
    def __init__(self, character):
        super().__init__(character)
        
    def enter(self):
        self.character.state = "hurt"
        self.start_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > 500:
            self.character.lock_actions = False
            self.character.state_machine.change_state("idle")
            
 
        
       