import random
import pygame
from .base_character import BaseCharacter

class Agent(BaseCharacter):
    def __init__(self, x, y, speed, sprite_dict):
        super().__init__(x, y, speed, sprite_dict)
        self.action_cooldown = 100
        self.action_probs = {
            "idle": 0.2,
            "move": 0.6, 
            "run": 0.0,
            "attack": 0.15,
            "defend": 0.1,
            "jump": 0.05
        }
        self.last_update_time = 0
        
    def update(self):
        # Handle cooldowns
        current_time = pygame.time.get_ticks()
        if self.action_cooldown > 0:
            self.action_cooldown -= current_time - self.last_update_time
        self.last_update_time = current_time
              
        self.ai_decide_action()
            
        super().update()  # Process current state
    
    def ai_decide_action(self):
        if random.random() < 0.7:  # 70% chance to act each cycle
            action = random.choices(
                list(self.action_probs.keys()),
                weights=list(self.action_probs.values())
            )[0]
            
            self.execute_ai_action(action)
            self.action_cooldown = 500  # 0.5s cooldown
    
    def execute_ai_action(self, action):
        """State transitions without any input dependencies"""
        if action == "move":
            self.facing_right = random.choice([True, False])
            self.state_machine.change_state("move")
            
        elif action == "run":
            self.facing_right = random.choice([True, False])
            self.state_machine.change_state("run")
            
        elif action == "attack":
            if self.state_machine.current_state_name == "run":
                self.state_machine.change_state("run_attack")
            else:
                self.state_machine.change_state("attack")
                
        elif action == "defend":
            self.state_machine.change_state("defend")
            
        elif action == "jump":
            self.state_machine.change_state("jump")