from typing import Literal
import pygame
import os

def cutting_sprite(character: Literal["freeza", "julian", "mark", "switch"], action: Literal["move", "run", "idle", "attack"], sprite_width=80, sprite_height=80):
    if action == "move":
        row_start = 0
        col_start = 4
        col_len = 4
        
    elif action == "idle":
        row_start = 0
        col_start = 0
        col_len = 4
    
    elif action == "attack":
        row_start = 1
        col_start = 0
        col_len = 4
    
    elif action == "run":
        row_start = 2
        col_start = 0
        col_len = 3
    
    path = "images/characters/{character}".format(character=character)
    image_sprite = pygame.image.load(os.path.join(path, "sprite.png")).convert_alpha()
    
    frame = pygame.Surface((sprite_width * col_len, sprite_height), pygame.SRCALPHA).convert_alpha()
    frame.blit(image_sprite, (0, 0), (col_start * sprite_width, row_start * sprite_height, sprite_width * col_len, sprite_height))
    pygame.image.save(frame, "{}/{}.png".format(path, action))
    print("Saved!")
 
   
def load_dict_from_folder(folder) -> dict:
    player = {}
    for filename in sorted(os.listdir(folder)):
        if filename != "sprite.png":
            img_path = os.path.join(folder, filename)
            img = pygame.image.load(img_path).convert_alpha()
            img.set_colorkey((0, 0, 0))
            action = filename.split(".")[0]
            player[action] = img
    return player