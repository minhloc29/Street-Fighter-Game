from .Abstract import State
import pygame

class DeadState(State):
    def __init__(self, character):
        super().__init__(character)
        self.lock_duration = 3000 
    def enter(self):
        self.character.state = "dead"
        self.death_time = pygame.time.get_ticks()
        
    def update(self):
        if pygame.time.get_ticks() - self.death_time > self.lock_duration:
            self.character.kill()  # Remove from sprite groups
    
        
       