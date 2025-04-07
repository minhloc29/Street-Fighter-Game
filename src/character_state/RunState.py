from .Abstract import State
import pygame
WIDTH, HEIGHT = 1280, 720

class RunState(State):
    def __init__(self, character):
        super().__init__(character)
        
    def enter(self):
        self.character.state = "run"
        self.character.speed = self.character.base_speed * 3
    
    def update(self):
        keys = pygame.key.get_pressed()
        moving = False
        
        # Vertical movement
        if keys[pygame.K_w]:
            if self.character.y - self.character.base_speed > 0:
                self.character.y -= self.character.base_speed
                moving = True
        if keys[pygame.K_s]:
            if self.character.y + 80 + self.character.base_speed < HEIGHT:
                self.character.y += self.character.base_speed
                moving = True

        # Horizontal movement
        if (self.character.facing_right and keys[pygame.K_a]) or \
           (not self.character.facing_right and keys[pygame.K_d]):
            self.character.state_machine.change_state("idle")
            return
            
        if self.character.facing_right:
            if self.character.x + 80 + self.character.speed < WIDTH:
                self.character.x += self.character.speed
                moving = True
        else:
            if self.character.x - self.character.speed > 0:
                self.character.x -= self.character.speed
                moving = True

        if not moving:
            self.character.state_machine.change_state("idle")
        elif keys[pygame.K_j]:
            self.character.state_machine.change_state("run_attack")
    
    def exit(self):
        self.character.speed = self.character.base_speed