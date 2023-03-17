"""
Sprites
"""
from pathlib import Path

import arcade
from attrs import define, field

from .constants import ASSETS_DIR


def get_sprite_path(parent: str, name: str) -> Path:
    """Gets the path for the sprite image"""
    return ASSETS_DIR / "sprites" / parent / f"{name.lower()}.png"


@define(slots=True, frozen=True)
class AttackSpec:
    """Class for defining an attack"""

    name: str
    desc: str
    base_atk_damage: float = field(converter=float)
    base_atk_cooldown: float = field(converter=float)
    base_proj_speed: float = field(converter=float)

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


class Enemy(arcade.Sprite):
    """Enemy sprite"""

    def __init__(self, name: str, desc: str, speed: float, scale: int = 1):
        """Enemy constructor"""

        self.name = name
        self.desc = desc
        self.speed = speed

        self.sprite_path = get_sprite_path("enemies", name)

        super().__init__(self.sprite_path, scale, hit_box_algorithm=None)


class Tower(arcade.Sprite):
    """Tower sprite"""

    # pylint: disable-next=too-many-arguments
    def __init__(
        self, name: str, desc: str, level: int, attacks: list[AttackSpec], scale: int = 1, radius: int = 100
    ):  # IDK if scale is important but it's in the docs https://github.com/e1pupper/tower
        """Tower constructor"""
        self.level = level
        self.radius = radius
        self.desc = desc

        self.sprite_path = get_sprite_path("towers", name)

        self.attacks = attacks

        super().__init__(self.sprite_path, scale, hit_box_algorithm=None)

    def show_range(self):
        """Shows the range of the tower"""
        arcade.draw_circle_outline(self.center_x, self.center_y, self.radius, arcade.color.BLACK, 2)

    def attack(self, enemy: Enemy):
        """
        Initiates an attack on the enemy when in circle range
        To do this all we need to do is check if the distance
        between the enemy and the tower is less than or equal to the radius
        """
        pass
