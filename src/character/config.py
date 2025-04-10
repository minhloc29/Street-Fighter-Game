from .animation import Animation

from src.character_state.IdleState import IdleState
from src.character_state.RunState import RunState
from src.character_state.MoveState import MoveState
from src.character_state.AttackState import AttackState
from src.character_state.RunAttackState import RunAttackState
from src.character_state.DefendState import DefendState
from src.character_state.JumpState import JumpState
from src.character_state.RunJumpState import RunJumpState
from src.character_state.DeadState import DeadState
from src.character_state.FallRightState import FallRightState
from src.character_state.FallLeftState import FallLeftState
from src.character_state.HurtState import HurtState

def get_animation_config(sprite_dict):
    return {
        "idle": Animation(sprite_dict["idle"], 300),
        "move": Animation(sprite_dict["move"], 150),
        "attack": Animation(sprite_dict["attack"], 230),
        "run": Animation(sprite_dict["run"], 150),
        "defend": Animation(sprite_dict["defend"], 300),
        "jump": Animation(sprite_dict["jump"], 250),
        "run_attack": Animation(sprite_dict["run_attack"], 120),
        "fall_left": Animation(sprite_dict["fall_left"], 100),
        "fall_right": Animation(sprite_dict["fall_right"], 100),
        "stand_up": Animation(sprite_dict["stand_up"], 150),
        "dead": Animation(sprite_dict["dead"], 150),
        "run_jump": Animation(sprite_dict["run_jump"], 200),
        "hurt": Animation(sprite_dict["hurt"], 200),
    }

def get_state_config(character):
    return {
        "idle": IdleState(character),
        "move": MoveState(character),
        "run": RunState(character),
        "attack": AttackState(character),
        "run_attack": RunAttackState(character),
        "defend": DefendState(character),
        "jump": JumpState(character),
        "fall_left": FallLeftState(character),
        "fall_right": FallRightState(character),
        "dead": DeadState(character),
        "run_jump": RunJumpState(character),
        "hurt": HurtState(character)
    }