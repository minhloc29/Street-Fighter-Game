import random
import pygame
from .character import Character
WIDTH, HEIGHT = 1280, 720

class AICharacter(Character):
    def __init__(self, x, y, speed, sprite_dict):
        super().__init__(x, y, speed, sprite_dict)
        self.last_action_time = pygame.time.get_ticks()
        self.action_interval = random.randint(500, 2000)  # random interval in ms
        self.move_direction = None  # "left" or "right"
    def update(self, player=None):
        current_time = pygame.time.get_ticks()
        self.update_cooldowns()

        # If not currently moving persistently, decide a new action
        if self.move_direction is None and current_time - self.last_action_time > self.action_interval:
            self.last_action_time = current_time
            self.action_interval = random.randint(500, 2000)
            action = random.choice(["move_left", "move_right", "attack", "defend", "jump", "idle", "run"])
            # print(f"[AI DEBUG] New action decided: {action}")  # Debug print

            if action == "run":
                self.start_running("right" if random.random() < 0.5 else "left")
                    
            if action == "move_left":
                self.move_direction = "left"
                self.facing_right = False
                self.state = "move"
                
            elif action == "move_right":
                self.move_direction = "right"
                self.facing_right = True
                self.state = "move"
            elif action == "attack":
                self.attack()
            elif action == "defend":
                self.defend()
            elif action == "jump":
                if not self.is_jumping:
                    self.jump()
            elif action == "idle":
                self.state = "idle"

        # If a movement direction is set, continue moving
        if self.move_direction is not None:
            if self.move_direction == "left":
                if self.x - self.base_speed > 0:
                    self.x -= self.base_speed
                    # print(f"[AI DEBUG] Moving left to {self.x}")  # Debug print
                else:
                    self.move_direction = None  # Stop if at left edge
            elif self.move_direction == "right":
                if self.x + 80 + self.base_speed < WIDTH:
                    self.x += self.base_speed
                    # print(f"[AI DEBUG] Moving right to {self.x}")  # Debug print
                else:
                    self.move_direction = None  # Stop if at right edge

            # Optionally, have a small chance to stop moving
            if random.random() < 0.01:
                
                self.move_direction = None
                self.state = "idle"

        if self.is_jumping:
            self.update_jump()

        
        