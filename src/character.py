import pygame
from .animation import Animation
WIDTH, HEIGHT = 1280, 720

class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, sprite_dict):
        super().__init__()
        # Position and movement
        self.x = x
        self.y = y
        self.base_speed = speed
        self.speed = speed
        self.state = "idle"
        self.facing_right = True
        self.is_running = False

        # For double-tap running logic (player-specific)
        self.last_press_d = 0
        self.last_press_a = 0

        # Jumping mechanics
        self.ground_y = y  # Ground level set to initial y
        self.is_jumping = False
        self.gravity = 1
        self.jump_velocity = -10

        # Attack and defend mechanics
        self.is_attacking = False
        self.attack_timer = 0
        self.is_defending = False
        self.defend_timer = 0

        # Build Animation objects from sprite sheets
        self.animations = {
            "idle": Animation(sprite_dict["idle"], 300),
            "move": Animation(sprite_dict["move"], 150),
            "attack": Animation(sprite_dict["attack"], 200),
            "run": Animation(sprite_dict["run"], 150),
            "defend": Animation(sprite_dict["defend"], 300),
            "jump": Animation(sprite_dict["jump"], 200),
            "run_attack": Animation(sprite_dict["run_attack"], 150)
        }
        
        # Health attributes
        self.max_health = 1000
        self.current_health = self.max_health
        self.is_dead = False

        # Create an initial image and hitbox (rect) based on the current animation frame
        self.image = self.animations[self.state].get_current_frame()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        # For running attack position update control
        self.has_updated_position = 0

    def draw(self, screen):
        if self.is_dead:
            return
        # Get current animation frame
        frame = self.animations[self.state].get_current_frame()
        # Flip frame if facing left
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        screen.blit(frame, (self.x, self.y))
        
        # Update the hitbox position
        self.rect.topleft = (self.x, self.y)
        
        # Draw health bar above the character
        health_bar_width = 50
        health_bar_height = 5
        health_ratio = self.current_health / self.max_health
        # Background of health bar (red)
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 10, health_bar_width, health_bar_height))
        # Foreground of health bar (green)
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 10, health_bar_width * health_ratio, health_bar_height))
        
    def jump(self):
        if not self.is_jumping:
            self.ground_y = self.y
            self.is_jumping = True
            self.state = "jump"
            self.jump_velocity = -10  # Reset jump impulse

    def update_jump(self):
        if self.is_jumping:
            self.y += self.jump_velocity
            # If running in air, update horizontal position accordingly
            if self.is_running:
                if self.facing_right:
                    self.x += self.speed
                else:
                    self.x -= self.speed
            self.jump_velocity += self.gravity
            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.is_jumping = False
                self.state = "idle"

    def start_running(self, direction):
        self.is_running = True
        self.state = "run"
        self.speed = self.base_speed * 3
        self.facing_right = (direction == "right")

    def attack(self, opponent=None):
        if self.is_running:
            self.state = "run_attack"
            self.is_attacking = True
            self.attack_timer = pygame.time.get_ticks()
            # Calculate duration based on animation settings
            self.run_attack_duration = self.animations["run_attack"].frame_num * self.animations["run_attack"].cooldown
            self.has_updated_position = 0
            
        elif not self.is_attacking:  # Avoid attack spamming
            self.is_attacking = True
            self.state = "attack"
            self.attack_timer = pygame.time.get_ticks()
        
        if opponent is not None:
            if pygame.sprite.collide_rect(self, opponent):
                opponent.take_damage(10)

    def defend(self):
        if not self.is_defending:  # Prevent spamming defend
            self.is_defending = True
            self.state = "defend"
            self.defend_timer = pygame.time.get_ticks()

    def update_cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.is_attacking and not self.is_running and current_time - self.attack_timer > 300:
            self.is_attacking = False
            self.state = "idle"
        elif self.is_attacking and self.is_running:
            # Update position a few times (once per frame until limit) during running attack
            if self.has_updated_position != 3:
                self.x = self.x + (15 if self.facing_right else -15)
                self.has_updated_position += 1
                
            if current_time - self.attack_timer > self.run_attack_duration:
                self.is_attacking = False
                self.is_running = False
                self.state = "idle"
                self.has_updated_position = 0
                
        if self.is_defending and current_time - self.defend_timer > 1000:
            self.is_defending = False
            self.state = "idle"

    def move(self, keys, opponent=None):
        collided_enemies = pygame.sprite.spritecollide(self, opponent, False)
        moving = False
        
        # Running movement logic
        if self.is_running:
            if keys[pygame.K_w]:
                if self.y - self.base_speed > 0:
                    self.y -= self.base_speed
                moving = True
            if keys[pygame.K_s]:
                if self.y + 80 + self.base_speed < HEIGHT:
                    self.y += self.base_speed
                moving = True
            
            if collided_enemies:
                return
          
            if (self.facing_right and keys[pygame.K_a]) or (not self.facing_right and keys[pygame.K_d]):
                moving = False
                self.is_running = False
                self.state = "idle"
            elif self.facing_right:
                if self.x + 80 + self.speed < WIDTH:
                    self.x += self.speed
                    moving = True
            else:
                if self.x - self.speed > 0:
                    self.x -= self.speed
                    moving = True


        # Normal (non-running) movement logic
        if not self.is_running:
            if keys[pygame.K_w]:
                if self.y - self.base_speed > 0:
                    self.y -= self.base_speed
                moving = True
            if keys[pygame.K_s]:
                if self.y + 80 + self.base_speed < HEIGHT:
                    self.y += self.base_speed
                moving = True
            
            if collided_enemies:
                return
            if keys[pygame.K_d]:
                self.facing_right = True
                if self.x + 80 + self.base_speed < WIDTH:
                    self.x += self.base_speed
                moving = True
            if keys[pygame.K_a]:
                self.facing_right = False
                if self.x - self.base_speed > 0:
                    self.x -= self.base_speed
                moving = True

        if moving:
            self.state = "run" if self.is_running else "move"
        else:
            self.state = "idle"
            self.is_running = False

    def take_damage(self, damage):
        """Reduce health by the specified amount and check for death."""
        self.current_health -= damage
        if self.current_health <= 0:
            self.current_health = 0
            self.is_dead = True
            self.state = "dead"
            print("Character is dead!")