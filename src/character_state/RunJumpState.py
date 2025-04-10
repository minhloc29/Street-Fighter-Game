from .Abstract import State
import pygame

class RunJumpState(State):
    def __init__(self, character):
        super().__init__(character)
        self.animation_duration = 1000
        self.leap_power = 7
        self.is_jumping = False
    def enter(self):
        print("Performing run jump")
        self.character.lock_actions = True
        self.start_time = pygame.time.get_ticks()
        self.character.state = "run_jump"
        self.ground_y = self.character.y
        self.is_jumping = True
        self.jump_velocity = -13
        self.gravity = 1
        # self.start
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.animation_duration:
            self.character.state_machine.change_state("idle")
        
        if self.is_jumping:
            self.character.y += self.jump_velocity
            self.character.x += self.character.base_speed * self.leap_power * (1 if self.character.facing_right else -1)
            self.jump_velocity += self.gravity
            
            if self.character.y >= self.ground_y:
                self.character.y = self.ground_y
                self.is_jumping = False
                self.character.lock_actions = False
                self.character.state_machine.change_state("idle")

       
    def exit(self):
       self.character.lock_actions = False