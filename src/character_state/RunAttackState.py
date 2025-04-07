from .Abstract import State
import pygame

class RunAttackState(State):
    def __init__(self, character):
        super().__init__(character)
        self.animation_duration = 1000  # ms
        self.leap_frames = 5           # Number of frames to apply leap
        self.current_leap = 0          # Current leap progress
        self.leap_power = 10           # Speed multiplier during leap

    def enter(self):
        self.start_time = pygame.time.get_ticks()
        self.character.state = "run_attack"
        self.current_leap = 0  # Reset leap counter
        # Optional: Play attack sound here
        # Optional: Set attack hitbox here

    def update(self):
        # Apply leap movement for first few frames
        if self.current_leap < self.leap_frames:
            direction = 1 if self.character.facing_right else -1
            self.character.x += self.character.base_speed * self.leap_power * direction
            self.current_leap += 1

        # Check if animation duration has completed
        if pygame.time.get_ticks() - self.start_time >= self.animation_duration:
            self.current_leap = 0
            self.character.state_machine.change_state("idle")
    
  