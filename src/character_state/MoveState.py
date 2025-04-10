from .Abstract import State
import pygame
WIDTH, HEIGHT = 1280, 720

class MoveState(State):
    def __init__(self, character):
        super().__init__(character)
        self.move_direction = (0, 0)
        
    def enter(self):
        self.character.state = "move"
        self.character.speed = self.character.base_speed
    
    def set_direction(self, x_dir, y_dir):
        self.move_direction = (x_dir, y_dir) 
        if x_dir != 0:
            self.facing_right = x_dir > 0   
    
    def update(self):
        # Apply movement based on current direction
        dx = self.move_direction[0] * self.character.speed
        dy = self.move_direction[1] * self.character.speed
        
        # Boundary checking
        new_x = self.character.x + dx
        new_y = self.character.y + dy
        
        self.character.x = new_x
        self.character.y = new_y
            
        # State transitions (no direct input checks)
        if self.move_direction == (0, 0):
            self.character.state_machine.change_state("idle")

        
        # def _detect_double_tap(self, keys):
            