"""Sprites"""

from importlib.resources import as_file

import arcade
from attrs import define, field

from .assets import get_sprite_path


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

        with as_file(get_sprite_path("enemies", f"{name}.png")) as file_path:
            super().__init__(file_path, scale, hit_box_algorithm=None)


class Tower(arcade.Sprite):
    """Tower sprite"""

    # pylint: disable-next=too-many-arguments
    def __init__(
        self, name: str, desc: str, level: int, attacks: list[AttackSpec], scale: int = 1, radius: int = 100
    ):  # IDK if scale is important but it's in the docs
        """Tower constructor"""
        self.level = level
        self.radius = radius
        self.desc = desc
        self.attacks = attacks

        with as_file(get_sprite_path("towers", f"{name}.png")) as file_path:
            super().__init__(file_path, scale, hit_box_algorithm=None)

    def show_range(self):
        """Shows the range of the tower"""
        arcade.draw_circle_outline(self.center_x, self.center_y, self.radius, arcade.color.BLACK, 2)

    def attack(self, enemy: Enemy):
        """
        Initiates an attack on the enemy when in circle range
        To do this all we need to do is check if the distance
        between the enemy and the tower is less than or equal to the radius
        """
