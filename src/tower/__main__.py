"""
Platformer Game
"""

import arcade
from .constants import LEVELS_DIR, SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.tile_map = None
        self.scene = None

        self.towers = None
        self.enemies = None

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        self.tile_map = arcade.load_tilemap(LEVELS_DIR / "level_1.tmx")

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.towers = arcade.SpriteList()
        self.enemies = arcade.SpriteList()

    def on_draw(self):
        """Render the screen."""

        self.clear()

        self.scene.draw()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
