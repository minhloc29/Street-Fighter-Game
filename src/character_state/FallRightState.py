from .Abstract import State
import pygame

class FallRightState(State):
    def __init__(self, character):
        super().__init__(character)
        self.character.animations["fall_right"].loop = False
        self.is_invulnerable = True
        self.leap_frames = 5
        self.current_frames = 0
    def enter(self, attacker = None):
        self.attacker = attacker
        self.character.state = "fall_right"
        self.is_invulnerable = True
        self.character.animations["fall_right"].reset()

    def update(self):
        if self.current_frames < self.leap_frames and self.attacker is not None:
            self.current_frames += 1
           
            if self.attacker.x > self.character.x:
                self.character.x -= 5
            else:
                self.character.x += 5
        
            
        if self.character.animations["fall_right"].is_complete():
            self.character.state_machine.change_state("idle")
            self.current_frames = 0
            self.character.lock_actions = False
            
    def exit(self):
        self.is_invulnerable = False
        self.current_frames = 0
        self.character.lock_actions = False
        
       