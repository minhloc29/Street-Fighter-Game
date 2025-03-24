import pygame

class Sprite:
    def __init__(self, image):
        self.sheet = image  # Store the sprite sheet

    def get_image(self, frame, width, height, row=0):
        """ Extracts a single frame from the sprite sheet. """
        image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), (frame * width, row * height, width, height))
        return image
    
class Animation:
    def __init__(self, sprite_image, cooldown): #idle, attack
        self.sprite_image = Sprite(sprite_image)
        self.last_update = pygame.time.get_ticks()
        self.cur_frame = 0
        self.cooldown = cooldown
        self.frame_num = sprite_image.get_width() // 80
        self.image_frame = self.sprite_image.get_image(self.cur_frame, 80, 80)


    def get_current_frame(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.cooldown:
            self.last_update = current_time
            self.cur_frame = (self.cur_frame + 1) % self.frame_num
            self.image_frame = self.sprite_image.get_image(self.cur_frame, 80, 80)
        return self.image_frame
            