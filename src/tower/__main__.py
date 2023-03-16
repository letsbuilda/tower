"""
Platformer Game
"""

from pathlib import Path

import arcade

# Constants
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 640
SCREEN_TITLE = "Platformer"


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

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        level_1_path = Path(__file__).parent.parent.parent / "assets" / "levels" / "level_1.tmx"
        self.tile_map = arcade.load_tilemap(level_1_path)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

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
