"""Game View"""

from pathlib import Path

import arcade
from tower import sprites


class GameView(arcade.View):
    """
    Main application class.
    """

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

        level_1_path = Path(__file__).parent.parent.parent / "assets" / "levels" / "level_1.tmx"
        self.tile_map = arcade.load_tilemap(level_1_path)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.towers = arcade.SpriteList()

        self.towers.append(sprites.Tower("tower1", "A basic tower", 1, [sprites.AttackSpec("Basic Attack", "A basic attack", 1, 1, 1)]))

        self.towers[0].center_x = self.scene.get_sprite_list('Tile Layer 1')[29].center_x
        self.towers[0].center_y = self.scene.get_sprite_list('Tile Layer 1')[29].center_y

        self.enemies = arcade.SpriteList()

    def on_draw(self):
        """Render the screen."""

        self.clear()

        self.scene.draw()

        self.towers.draw()
        self.towers[0].show_range()
