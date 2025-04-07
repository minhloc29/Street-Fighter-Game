from .Abstract import State
import pygame

class AttackState(State):
    def __init__(self, character):
        super().__init__(character)
        self.press_start = False
        self.press_end = False
        self.animation_duration = 300
        
    def enter(self):
        self.press_start = True
        self.start_time = pygame.time.get_ticks()
        self.character.state = "attack"
        self.character.speed = 0
    
    def update(self):
        
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.animation_duration:
            self.character.state_machine.change_state("idle")
        
        if not self.press_start:
            self.character.state_machine.change_state("idle")
       
    def exit(self):
        self.character.speed = self.character.base_speed