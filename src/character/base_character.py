import pygame
from .animation import Animation

from src.character_state.IdleState import IdleState
from src.character_state.RunState import RunState
from src.character_state.MoveState import WalkState
from src.character_state.AttackState import AttackState
from src.character_state.RunAttackState import RunAttackState
from src.character_state.DefendState import DefendState
from src.character_state.JumpState import JumpState
from src.character_state.state_machine import StateMachine

class BaseCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, sprite_dict):
        super().__init__()
        
        self.state_machine = StateMachine(self)
        self._init_states()
        
        self.x = x
        self.y = y
        self.facing_right = True
        self.speed = speed
        self.base_speed = speed
        
        self.state = "idle"
        
        self.animations = {
            "idle": Animation(sprite_dict["idle"], 300),
            "move": Animation(sprite_dict["move"], 150),
            "attack": Animation(sprite_dict["attack"], 250),
            "run": Animation(sprite_dict["run"], 150),
            "defend": Animation(sprite_dict["defend"], 300),
            "jump": Animation(sprite_dict["jump"], 200),
            "run_attack": Animation(sprite_dict["run_attack"], 150),
            "fall": Animation(sprite_dict["fall"], 150),
            "stand_up": Animation(sprite_dict["stand_up"], 150),
        }
    
    def _init_states(self):
        self.state_machine.add_state("idle", IdleState(self))
        self.state_machine.add_state("move", WalkState(self))
        self.state_machine.add_state("run", RunState(self))
        self.state_machine.add_state("attack", AttackState(self))
        self.state_machine.add_state("run_attack", RunAttackState(self))
        self.state_machine.add_state("defend", DefendState(self))
        self.state_machine.add_state("jump", JumpState(self))
    
    def update(self):
        self.state_machine.update()
    
    def draw(self, screen):
        frame = self.animations[self.state_machine.current_state_name].get_current_frame()
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        screen.blit(frame, (self.x, self.y))
        
        
        