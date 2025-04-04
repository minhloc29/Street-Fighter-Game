import pygame
from .character import Character
class PlayerCharacter(Character):
    def update(self, keys, events, enemy_group):
        current_time = pygame.time.get_ticks()

        # Handle player input events
        for event in events:
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()  # refresh key state for each event
                if event.key == pygame.K_d:
                    if current_time - self.last_press_d < 300:
                        self.start_running("right")
                    self.last_press_d = current_time
                elif event.key == pygame.K_a:
                    if current_time - self.last_press_a < 300:
                        self.start_running("left")
                    self.last_press_a = current_time
                elif event.key == pygame.K_j:
                    self.attack()
                elif event.key == pygame.K_k:
                    self.defend()
                elif event.key == pygame.K_l:
                    if not self.is_jumping:
                        self.jump()

        # Update attack/defense cooldowns
        self.update_cooldowns()

        # Handle movement if not busy with an attack, defense, or jump
        if not (self.is_attacking or self.is_defending or self.is_jumping):
            self.move(keys, enemy_group)

        # Update jumping mechanics if in the air
        if self.is_jumping:
            self.update_jump()