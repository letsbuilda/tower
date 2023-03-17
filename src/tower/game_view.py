"""Game View"""
from importlib.resources import as_file

import arcade

from . import sprites
from .assets import get_tile_map_path


class GameView(arcade.View):
    """Main application class."""

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__()
        self.window.set_mouse_visible(False)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.tile_map = None
        self.scene = None

        self.towers = None
        self.enemies = None

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        with as_file(get_tile_map_path("level_1.tmx")) as file_path:
            self.tile_map = arcade.load_tilemap(file_path)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.towers = arcade.SpriteList()

        self.towers.append(
            sprites.Tower("tower1", "A basic tower", 1, [sprites.AttackSpec("Basic Attack", "A basic attack", 1, 1, 1)])
        )

        self.towers[0].center_x = self.scene.get_sprite_list("Tile Layer 1")[29].center_x
        self.towers[0].center_y = self.scene.get_sprite_list("Tile Layer 1")[29].center_y

        self.enemies = arcade.SpriteList()

    def on_draw(self):
        """Render the screen."""

        self.clear()

        self.scene.draw()

        self.towers.draw()
        self.towers[0].show_range()
