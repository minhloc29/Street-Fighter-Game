from .Abstract import State
import pygame

class JumpState(State):
    def __init__(self, character):
        super().__init__(character)
        self.animation_duration = 1000
        self.is_jumping = False
    def enter(self):
        
        self.start_time = pygame.time.get_ticks()
        self.character.state = "jump"
        
        self.ground_y = self.character.y
        self.is_jumping = True
        self.jump_velocity = -10
        self.gravity = 1
        # self.start
    def update(self):
        # current_time = pygame.time.get_ticks()
        # if current_time - self.start_time >= self.animation_duration:
        #     self.character.state_machine.change_state("idle")
        
        if self.is_jumping:
            self.character.y += self.jump_velocity
            self.jump_velocity += self.gravity
            
            if self.character.y >= self.ground_y:
                self.character.y = self.ground_y
                self.is_jumping = False
                self.character.state_machine.change_state("idle")

       
    def exit(self):
       self.character.y = self.ground_y