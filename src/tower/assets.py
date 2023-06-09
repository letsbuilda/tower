"""Utilities for loading assets"""

from importlib.abc import Traversable
from importlib.resources import files

from .constants import MAP_WIDTH


def get_asset_path(*paths: str) -> Traversable:
    """Gets the path for an asset"""
    file_path = files("tower").joinpath("assets")
    for path in paths:
        file_path = file_path.joinpath(path)
    return file_path


def get_sprite_path(parent: str, name: str) -> Traversable:
    """Gets the path for the sprite image"""
    return get_asset_path("sprites", parent, name)


def get_tile_map_path(name: str) -> Traversable:
    """Gets the path for a tile map"""
    return get_asset_path("levels", name)


def coord_to_index(x_coord: int, y_coord: int) -> int:
    """Turns an (x, y) coordinate into an index for the tile map"""
    return MAP_WIDTH * x_coord + y_coord
