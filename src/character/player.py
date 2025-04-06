from .base_character import BaseCharacter
import pygame

class PlayerCharacter(BaseCharacter):
    # facing right = True from BaseCharacter
    def __init__(self, x, y, speed, sprite_dict):
        super().__init__(x, y, speed, sprite_dict)
        self.last_input_time = {
            'A': 0,
            'D': 0
        }
        self.double_tap_threshold = 300
        self.is_running = False
        
        self.is_attack = False
        
    def update(self, events):
        self.handle_input(events)
        super().update()
    
    def double_tap_detected(self, key, current_time):
        time_since_last = current_time - self.last_input_time[key]
        self.last_input_time[key] = current_time
        
        if time_since_last < self.double_tap_threshold:
            return True
        return False

        
    def handle_input(self, events):
        current_time = pygame.time.get_ticks()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and self.double_tap_detected('D', current_time):
                    self.facing_right = True
                    self.state_machine.change_state("run")
                    print(self.state_machine.current_state_name)
                    
                elif event.key == pygame.K_a and self.double_tap_detected('A', current_time):
                    self.facing_right = False
                    self.state_machine.change_state("run")
                    print(self.state_machine.current_state_name)
                    
                elif event.key in (pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s) and self.state_machine.current_state_name != "run":
                    self.state_machine.change_state("move")
                         
                if event.key == pygame.K_j:
                    if self.state_machine.current_state_name == "run":
                        self.state_machine.change_state("run_attack")
                    else:
                        self.state_machine.change_state("attack")
                
                if event.key == pygame.K_k:
                    self.state_machine.change_state("defend")
                
                