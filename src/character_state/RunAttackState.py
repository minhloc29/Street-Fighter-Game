from .Abstract import State
import pygame

class RunAttackState(State):
    def __init__(self, character):
        super().__init__(character)
        # self.animation_duration = 1000  # ms
        self.leap_frames = 5           # Number of frames to apply leap
        self.current_leap = 0          # Current leap progress
        self.leap_power = 10           # Speed multiplier during leap
        self.character.animations["run_attack"].loop = False
    def enter(self):
        self.character.lock_actions = True
        self.character.state = "run_attack"
        self.current_leap = 0  # Reset leap counter
        # Optional: Play attack sound here
        # Optional: Set attack hitbox here
        self.character.animations["run_attack"].reset()
    def update(self):
        # Apply leap movement for first few frames
        if self.current_leap < self.leap_frames:
            direction = 1 if self.character.facing_right else -1
            self.character.x += self.character.base_speed * self.leap_power * direction
            self.current_leap += 1
        if self.character.animations["run_attack"].is_complete():
            print("complete run attack")
            self.character.lock_actions = False
            self.character.state_machine.change_state("idle")
    
    def exit(self):
        self.character.lock_actions = False
    
    
  