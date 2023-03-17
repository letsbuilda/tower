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

        self.enemies = sprites.EnemyList()

        # calculate the path enemies should follow (This only has to be done once)
        position_list = self.calculate_enemy_path()

        # create dummy enemy
        enemy = sprites.Enemy("enemy_1", "Dummy enemy to test following a path", 2, position_list)

        # Set initial location of the enemy at the first point
        enemy.center_x = position_list[0][0]
        enemy.center_y = position_list[0][1]

        self.enemies.append(enemy)

    def on_draw(self):
        """Render the screen."""

        self.clear()

        self.scene.draw()

        self.towers.draw()
        self.towers[0].show_range()

        self.enemies.draw()

    def on_update(self, delta_time: float):
        """Updates the position of all enemies"""
        self.enemies.update()

    def calculate_enemy_path(self) -> list[tuple[int]]:
        """calculates the path enemies should follow
        returns a list of tuples (x, y) representing a coordinate of the path
        that the enemy follows
        """
        position_list = []
        all_sprites = self.scene.get_sprite_list("Tile Layer 1")
        tile_map = self.tile_map.get_tilemap_layer("Tile Layer 1").data

        row, col = self._find_start_index(tile_map)

        visited = [[False for _ in range(len(tile_map[0]))] for _ in range(len(tile_map))]

        # while the end of the path is not reached
        while all_sprites[row * len(tile_map[0]) + col].properties["tile_id"] != 5:
            # add current position to position list
            # get sprite of row and col
            sprite = all_sprites[row * len(tile_map[0]) + col]
            position_list.append((sprite.center_x, sprite.center_y))
            visited[row][col] = True
            # get next path position
            row, col = self.get_next_path_position(row, col, tile_map, visited)

        sprite = all_sprites[row * len(tile_map[0]) + col]
        position_list.append((sprite.center_x, sprite.center_y))
        return position_list

    def _find_start_index(self, tile_map):
        """returns the index of the tile that represents the start of the path"""
        start_sprites = [5]
        for row_index, row in enumerate(tile_map):
            for col_index, col in enumerate(row):
                if col in start_sprites:
                    return row_index, col_index
        return None, None

    def get_next_path_position(self, row, col, tile_map, visited) -> int:
        """Returns the next path position
        assumes that there is only one possible path
        """
        # has all id's of paths
        path_blocks = [3, 6, 5]

        # check top neighbor
        if row > 0:
            if tile_map[row - 1][col] in path_blocks and not visited[row - 1][col]:
                return row - 1, col

        # check bottom neighbor
        if row < len(tile_map) - 1:
            if tile_map[row + 1][col] in path_blocks and not visited[row + 1][col]:
                return row + 1, col

        # check left neighbor
        if col > 0:
            if tile_map[row][col - 1] in path_blocks and not visited[row][col - 1]:
                return row, col - 1

        # check right neighbor
        if col < len(tile_map[0]) - 1:
            if tile_map[row][col + 1] in path_blocks and not visited[row][col + 1]:
                return row, col + 1
        return -1, -1
