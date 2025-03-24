from .animation import Animation

class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.base_speed = speed
        self.speed = speed  # Maintain current speed separately
        self.state = "idle"
        self.facing_right = True
        self.press_d = 0
        self.press_a = 0
        self.animations = {
            "idle": Animation(player_dict["idle"], 100),
            "move": Animation(player_dict["move"], 100),
            "attack": Animation(player_dict["attack"], 150),
            "run": Animation(player_dict["run"], 150),
        }

    def move(self, keys):
        move = False
        current_time = pygame.time.get_ticks()

        # **Move Right ("D")**
        if keys[pygame.K_d]:
            self.facing_right = True
            if current_time - self.press_d < 300:  # Detects double-tap
                self.speed = self.base_speed * 3
                self.state = "run"
            else:
                self.speed = self.base_speed
                self.state = "move"

            if self.x + 80 + self.speed < WIDTH:
                self.x += self.speed
            self.press_d = current_time  # Update time of last press
            move = True

        # **Move Left ("A")**
        elif keys[pygame.K_a]:
            self.facing_right = False
            if current_time - self.press_a < 300:
                self.speed = self.base_speed * 3
                self.state = "run"
            else:
                self.speed = self.base_speed
                self.state = "move"

            if self.x - self.speed > 0:
                self.x -= self.speed
            self.press_a = current_time
            move = True

        # **Move Up ("W")**
        elif keys[pygame.K_w]:
            if self.y - self.base_speed > 0:
                self.y -= self.base_speed
            self.state = "move"
            move = True

        # **Move Down ("S")**
        elif keys[pygame.K_s]:
            if self.y + 80 + self.base_speed < HEIGHT:
                self.y += self.base_speed
            self.state = "move"
            move = True

        # **Attack ("J")**
        elif keys[pygame.K_j]:
            self.state = "attack"
            move = True

        # **Reset to Idle if No Movement**
        if not move:
            self.state = "idle"
            self.speed = self.base_speed  # Reset speed when stopping

        print(f"State: {self.state}, Position: ({self.x}, {self.y}), Speed: {self.speed}")

    def draw(self, screen):
        frame = self.animations[self.state].get_current_frame()
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        screen.blit(frame, (self.x, self.y))
