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

    def atk_cooldown(self, level: int) -> float:
        """Calculates the cooldown of the attack"""
        return self.base_atk_cooldown / level

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
    def __init__(self, name: str, desc: str, speed: float, health: int, position_list: list, scale: int = 1):
        """Enemy constructor"""
        self.name = name
        self.desc = desc
        self.speed = speed
        self._health = health
        self.position_list = position_list
        self.current_position = 0
        self.is_alive = True

        with as_file(get_sprite_path("enemies", f"{name}.png")) as file_path:
            super().__init__(file_path, scale)

    @property
    def health(self):
        """Health getter"""
        return self._health

    @health.setter
    def health(self, value: int):
        """Health setter"""
        if value <= 0:
            self.is_alive = False
        self._health = value

    def update(self):
        """calculates new position of enemy but only when it is alive"""
        if not self.is_alive:
            self.remove_from_sprite_lists()
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
        self, name: str, desc: str, level: int, attacks: list[AttackSpec], radius: int = 100, scale: int = 1
    ):  # IDK if scale is important but it's in the docs
        """Tower constructor"""
        self.level = level
        self.radius = radius
        self.desc = desc
        self.attack_cooldowns = {attack: 0 for attack in attacks}
        self.current_target = None

        # Add attacks here to be processed later in GameView
        self.pending_attacks = []

        with as_file(get_sprite_path("towers", f"{name}.png")) as file_path:
            super().__init__(file_path, scale, hit_box_algorithm=None)

    def show_range(self):
        """Shows the range of the tower"""
        arcade.draw_circle_outline(self.center_x, self.center_y, self.radius, arcade.color.BLACK, 2)

    def attack(self, attack: AttackSpec):
        """
        Fires an attack at self.current_target
        Assumes target is in range
        """
        self.pending_attacks.append(Projectile((self.center_x, self.center_y), attack, self.level, self.current_target))

    def get_enemy_dist(self, enemy: Enemy) -> float:
        """Get distance from tower to enemy"""
        return math.dist(self.position, enemy.position)

    def update(self):
        """
        Updates attacks on target
        Assumes target is in range
        """
        if not self.current_target:
            return
        for attack, cooldown in self.attack_cooldowns.items():
            # Cooldown is over
            if not cooldown:
                self.attack(attack)
                self.attack_cooldowns[attack] = attack.atk_cooldown(self.level)
            # Decrement cooldown
            else:
                self.attack_cooldowns[attack] -= 1


class Projectile(arcade.Sprite):
    """Projectile sprite"""

    # pylint: disable-next=too-many-arguments
    def __init__(self, position: tuple[float, float], attack: AttackSpec, level: int, target: Enemy, scale: int = 0.2):
        """Projectile constructor"""
        self.attack = attack
        self.target = target
        self.speed = attack.proj_speed(level)
        self.level = level

        with as_file(get_sprite_path("projectiles", f"{self.attack.name}.png")) as file_path:
            super().__init__(file_path, scale)

        self.center_x, self.center_y = position

    def get_enemy_dist(self, enemy: Enemy) -> float:
        """Gets distance from projectile to enemy"""
        return math.dist(self.position, enemy.position)

    def update(self):
        """Update function"""
        # If it has hit the target
        if self.collides_with_point(self.target.position):
            self.target.health -= self.attack.atk_damage(self.level)
            self.remove_from_sprite_lists()

        angle = math.atan2(self.target.center_y - self.center_y, self.target.center_x - self.center_x)
        self.velocity = self.speed * math.cos(angle), self.speed * math.sin(angle)
        super().update()
