"""Sprites"""

import math
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


class EnemyList(arcade.SpriteList):
    """A list of enemies"""

    # pylint: disable=W0622
    def draw(self, *, filter=None, pixelated=None, blend_function=None):
        """Draws only enemies that are alive"""
        for sprite in self:
            if sprite.is_alive:
                sprite.draw()


# pylint: disable=too-many-instance-attributes
class Enemy(arcade.Sprite):
    """Enemy sprite"""

    # pylint: disable=too-many-arguments
    def __init__(self, name: str, desc: str, speed: float, position_list: list, scale: int = 1):
        """Enemy constructor"""
        self.name = name
        self.desc = desc
        self.speed = speed
        self.position_list = position_list
        self.current_position = 0
        self.is_alive = True

        with as_file(get_sprite_path("enemies", f"{name}.png")) as file_path:
            super().__init__(file_path, scale, hit_box_algorithm=None)

    def update(self):
        """calculates new position of enemy but only when it is alive"""
        if not self.is_alive:
            return
        # current position
        start_x = self.center_x
        start_y = self.center_y

        # get next destination position
        destination_x, destination_y = self.position_list[self.current_position]

        # X and Y diff between the two
        x_diff = destination_x - start_x
        y_diff = destination_y - start_y

        # Calculate angle to get there
        angle = math.atan2(y_diff, x_diff)

        # Calculate vector to travel
        change_x = math.cos(angle) * self.speed
        change_y = math.sin(angle) * self.speed

        # Update our location
        self.center_x += change_x
        self.center_y += change_y

        # get distance to destination
        distance = math.sqrt((self.center_x - destination_x) ** 2 + (self.center_y - destination_y) ** 2)

        # If we are there, head to the next point.
        if distance <= self.speed:
            self.current_position += 1

            # Reached the end of the list --> remove it
            if self.current_position >= len(self.position_list):
                self.is_alive = False


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
