from typing import Literal
import pygame
import os

def cutting_sprite(character: Literal["freeza", "julian", "mark", "switch"], action: Literal["move", "run", "idle", "attack", "defend", "jump"], pos, sprite_width=80, sprite_height=80):
    #pos is like: [[1, 2], [2, 3]] the postion of sprite to extract
    path = "images/characters/{character}".format(character=character)
    image_sprite = pygame.image.load(os.path.join(path, "sprite.png")).convert_alpha()
    
    frame = pygame.Surface((sprite_width * len(pos), sprite_height), pygame.SRCALPHA).convert_alpha()
    for idx, cur_pos in enumerate(pos):
        frame.blit(image_sprite, (idx * sprite_width, 0), (cur_pos[1] * sprite_width, cur_pos[0] * sprite_height, sprite_width, sprite_height))
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