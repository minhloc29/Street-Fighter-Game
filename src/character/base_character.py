import pygame
from .animation import Animation
from .config import get_animation_config, get_state_config
from src.character_state.state_machine import StateMachine
WIDTH, HEIGHT = 1280, 720

class BaseCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, sprite_dict, name):
        super().__init__()
        
        self.name = name
        self.width = 80
        self.height = 80 # frame pixel size from sprite 
        self.x = x
        self.y = y
        self.facing_right = True
        self.speed = speed
        self.base_speed = speed
        self.lock_actions = False
        
        self.damage_received = 0
        self.damage_threshold = 40
        self.state = "idle"
        
        self.visible_frames = 100
        self.cur_frames = 0
        self.complete_recovery = False
        
        self.animations = get_animation_config(sprite_dict)
        
        self.state_machine = StateMachine(self)
        self._init_states()
        
        #health attributes
        self.max_health = 10000
        self.current_health = self.max_health
        # Create an initial image and hitbox (rect) based on the current animation frame
        self.image = self.animations[self.state].get_current_frame()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)
    
    def _init_states(self):
       for state_name, state in get_state_config(self).items():
            self.state_machine.add_state(state_name, state)
    
    def check_within_screen(self):
        if self.x >= WIDTH - self.width:
            self.x = WIDTH - self.width
        elif self.x <= 0:
            self.x = 0
        if self.y >= HEIGHT - self.height:
            self.y = HEIGHT - self.height
        elif self.y <= 0:
            self.y = 0
            
    def update(self):
        self.check_within_screen()    
        self.state_machine.update()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        self.draw_shadow(screen)
        self.draw_health_bar(screen)
        self.cur_frames = (self.cur_frames + 1) % self.visible_frames
        if (self.state_machine.previous_state_name == "fall_left" \
        or self.state_machine.previous_state_name == "fall_right") \
        and self.cur_frames % 5 != 0:
            return
        if self.cur_frames == 0:
            self.complete_recovery = True
            
        frame = self.animations[self.state_machine.current_state_name].get_current_frame()
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        screen.blit(frame, (self.x, self.y))
        
    def draw_shadow(self, screen):
        shadow_offset = 2
        shadow_alpha = 100
        shadow = pygame.Surface((self.width - 15, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, shadow_alpha), (0, 0, self.width-20, 10))
        shadow_x = self.x + 15 + (self.width / 2) - (shadow.get_width() / 2)
        shadow_y = self.y + self.height + 21  # Slightly above ground level
        screen.blit(shadow, (shadow_x, shadow_y))
    
    
    def take_damage(self, amount, collided_agent=None):
        if self._is_invulnerable():
            return 
        
        self.complete_recovery = False
        self.damage_received += amount
        self.current_health -= self.damage_received
        
        if self.current_health <= 0:
            self.state_machine.change_state("dead")
            return
        
        current_state = self.state_machine.current_state_name
        if current_state != "hurt":
            self.state_machine.change_state("hurt")
        
        
        if self.current_health > 0 and current_state not in ["fall_right", "fall_left", "dead"] and self.damage_received >= self.damage_threshold:
            self.trigger_fall_state(collided_agent)
            
        if self.damage_received >= self.damage_threshold / 2:
            self.lock_actions = True
            
    def trigger_fall_state(self, collided_agent):
            # Fall away from collided_agent
        print(f"Received damage: {self.damage_received}")
        self.damage_received = 0
        self.lock_actions = True
        if (self.facing_right and not collided_agent.facing_right) or (not self.facing_right and collided_agent.facing_right):
            fall_state = "fall_left"
        else:
            fall_state = "fall_right"
    
      
        self.state_machine.change_state(fall_state, collided_agent)
        
    
    def _is_invulnerable(self):

        return (self.current_health <= 0 or 
                self.state_machine.current_state_name in ["fall_right", "fall_left", "defend", "dead"])
    
    
    def draw_health_bar(self, screen):
        bar_width = 50
        bar_height = 8
        
        fill = max(0, (self.current_health / self.max_health) * bar_width)
    
        #position of the bar
        bar_x = self.x + 25
        bar_y = self.y + 5
        #draw the bar
        pygame.draw.rect(screen, (30, 30, 30), (bar_x, bar_y - bar_height, bar_width, bar_height))
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y - bar_height, fill, bar_height))
    
    def handle_collisions(self, collisions):
        if self.current_health <= 0:
            return
        for collided_agent in collisions:
            if collided_agent.name != self.name:
            
            # Let take_damage() handle state transitions
                if collided_agent.state_machine.previous_state_name in ["fall_left", "fall_right"] and not collided_agent.complete_recovery:
                    pass
                
                elif self.state_machine.current_state_name == "attack" and self.animations["attack"].cur_frame in [1, 3]:  
                    collided_agent.take_damage(10, self)
                elif self.state_machine.current_state_name == "run_attack" and self.animations["run_attack"].cur_frame in [2, 6]:
                    collided_agent.take_damage(20, self)
