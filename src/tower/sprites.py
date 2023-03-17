"""
Sprites
"""
from pathlib import Path

import arcade
from attrs import define, field

from .constants import ASSETS_DIR


@define(slots=True, frozen=True)
class AttackSpec:
    """Class for defining an attack"""

    name: str
    desc: str
    base_atk_damage: float = field(converter=float)
    base_atk_cooldown: float = field(converter=float)
    base_proj_speed: float = field(converter=float)

    def get_sprite_path(self) -> Path:
        """Gets the path for the projectile sprite image"""
        return ASSETS_DIR / "sprites" / "projectiles" / f"{self.name.lower()}.png"

    # These three should scale off of level
    # Proper scaling can come later after we actually implement gameplay
    def atk_damage(self, level: int) -> float:
        """Calculates the damage of the attack"""
        return self.base_atk_damage * level

    def atk_speed(self, level: int) -> float:
        """Calculates the cooldown of the attack"""
        return self.base_atk_cooldown * level

    def proj_speed(self, level: int) -> float:
        """Calculates the speed of the projectile"""
        return self.base_proj_speed * level


class Tower(arcade.Sprite):
    """Tower sprite"""

    # pylint: disable-next=too-many-arguments
    def __init__(
        self, 
        name: str, 
        desc: str, 
        level: int, 
        attacks: list[AttackSpec], 
        scale: int = 1,
        radius: int = 100
    ):  # IDK if scale is important but it's in the docs https://github.com/e1pupper/tower
        """Tower constructor"""
        super().__init__(name, desc, scale)

        self.level = level
        self.radius = radius

        self.sprite_path = Path(__file__).parent.parent.parent / "assets" / "sprites" / "towers" / f"{name}.png"

        self.attacks = attacks

        super().__init__(self.sprite_path, scale, hit_box_algorithm=None)


class Enemy(arcade.Sprite):
    """Enemy sprite"""

    def __init__(self, name: str, desc: str, speed: float, scale: int = 1):
        """Enemy constructor"""

        self.name = name
        self.desc = desc
        self.speed = speed

        self.sprite_path = Path(__file__).parent.parent.parent / "assets" / "sprites" / "enemies" / f"{name}.png"

        super().__init__(self.sprite_path, scale, hit_box_algorithm=None)
