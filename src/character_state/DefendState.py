from .Abstract import State
import pygame

class DefendState(State):
    def __init__(self, character):
        super().__init__(character)
        self.cooldown = 1000
        
    def enter(self):
        self.character.state = "defend"
        self.character.speed = 0
        self.start_time = pygame.time.get_ticks()
        
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.cooldown:
            self.character.state_machine.change_state("idle")
    
        
       