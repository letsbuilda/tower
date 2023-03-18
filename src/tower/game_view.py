"""Game View"""

from importlib.resources import as_file

import arcade

from . import sprites
from .assets import coord_to_index, get_tile_map_path
from .constants import END_SPRITE_IDS, PATH_SPRITE_IDS, START_SPRITE_IDS


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
        self.active_projectiles = None

        # calculate the path enemies should follow (This only has to be done once)
        self.position_list = self.calculate_enemy_path()

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        with as_file(get_tile_map_path("level_1.tmx")) as file_path:
            self.tile_map = arcade.load_tilemap(file_path)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.towers = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.active_projectiles = arcade.SpriteList()

        # Temporary stuff
        test_tower = sprites.Tower(
            "tower1", "A basic tower", 1, [sprites.AttackSpec("Fireball", "A basic fireball", 25, 10, 5)], 300
        )
        test_tile = self.scene.get_sprite_list("Tile Layer 1")[coord_to_index(7, 11)]
        test_tower.center_x = test_tile.center_x
        test_tower.center_y = test_tile.center_y
        self.towers.append(test_tower)

        # create dummy enemy
        arcade.schedule(self.temp_add_enemy, 1)

    def on_draw(self):
        """Render the screen."""

        self.clear()

        self.scene.draw()

        self.towers.draw()
        self.towers[0].show_range()

        self.enemies.draw()

        self.active_projectiles.draw()

    def on_update(self, delta_time: float):
        """Updates the position of all enemies"""
        self.enemies.update()

        # Update tower targets
        for tower in self.towers:
            # If tower is already targeting, check if enemy is still in range
            if tower.current_target and tower.get_enemy_dist(tower.current_target) < tower.radius:
                continue
            # Find target (closest enemy to tower)
            target = None
            current_min_dist = float("inf")
            for enemy in self.enemies:
                dist = tower.get_enemy_dist(enemy)
                # Checks if enemy is in range and is closest to tower
                if tower.radius > dist < current_min_dist:
                    target = enemy
                    current_min_dist = dist

            # Set new target
            tower.current_target = target
        self.towers.update()
        for tower in self.towers:
            for projectile in tower.pending_attacks:
                self.active_projectiles.append(projectile)
            tower.pending_attacks.clear()

        self.active_projectiles.update()

        # Check that all enemies targeted are still alive
        for tower in self.towers:
            if tower.current_target is not None and not tower.current_target.is_alive:
                tower.current_target = None

        # If any projectiles are targeting dead enemies, find the next closest enemy and go for them
        for projectile in self.active_projectiles:
            if not projectile.target.is_alive:
                if self.enemies:
                    projectile.target = min(self.enemies, key=projectile.get_enemy_dist)
                else:
                    projectile.remove_from_sprite_lists()

    def calculate_enemy_path(self) -> list[tuple[int, int]]:
        """calculates the path enemies should follow
        returns a list of tuples (x, y) representing a coordinate of the path
        that the enemy follows
        """
        # contains all coordinates in the form (x, y), that the enemies should follow
        position_list = []

        # this is a 1D representation of our map containing sprites
        all_sprites = self.scene.get_sprite_list("Tile Layer 1")

        # this is a 2D representation of our map containing only the id of the sprite
        tile_map = self.tile_map.get_tilemap_layer("Tile Layer 1").data

        # get the position of the start block
        row, col = self._find_start_index(tile_map)

        # visited keeps track whether we already visited tile_map[row][col]
        visited = [[False for _ in range(len(tile_map[0]))] for _ in range(len(tile_map))]

        # while the end of the path is not reached
        while tile_map[row][col] not in END_SPRITE_IDS:
            # add current position to position list
            # get sprite of row and col by calculating its 1D position
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
        for row_index, row in enumerate(tile_map):
            for col_index, col in enumerate(row):
                if col in START_SPRITE_IDS:
                    return row_index, col_index
        return None, None

    def get_next_path_position(self, row, col, tile_map, visited) -> tuple[int, int]:
        """Returns the next path position
        assumes that there is only one possible path
        """

        # check top neighbor
        if row > 0:
            if tile_map[row - 1][col] in PATH_SPRITE_IDS and not visited[row - 1][col]:
                return row - 1, col

        # check bottom neighbor
        if row < len(tile_map) - 1:
            if tile_map[row + 1][col] in PATH_SPRITE_IDS and not visited[row + 1][col]:
                return row + 1, col

        # check left neighbor
        if col > 0:
            if tile_map[row][col - 1] in PATH_SPRITE_IDS and not visited[row][col - 1]:
                return row, col - 1

        # check right neighbor
        if col < len(tile_map[0]) - 1:
            if tile_map[row][col + 1] in PATH_SPRITE_IDS and not visited[row][col + 1]:
                return row, col + 1
        return -1, -1

    # pylint: disable-next=unused-argument
    def temp_add_enemy(self, delta_time: float):
        """Temporary function for testing enemies"""
        enemy = sprites.Enemy("enemy_1", "Dummy enemy to test following a path", 2, 50, self.position_list)

        # Set initial location of the enemy at the first point
        enemy.center_x, enemy.center_y = self.position_list[0]

        self.enemies.append(enemy)
