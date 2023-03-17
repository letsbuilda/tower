"""Game View"""

from pathlib import Path

import arcade


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
        self.enemies = arcade.SpriteList()

    def on_draw(self):
        """Render the screen."""

        self.clear()

        self.scene.draw()
