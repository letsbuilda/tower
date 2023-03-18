"""Variables that are needed in multiple files and don't change."""

# Screen
SCREEN_WIDTH = 24 * 64
SCREEN_HEIGHT = 15 * 64
SCREEN_TITLE = "Platformer"

# ID's of our path start sprites in the data csv
START_SPRITE_IDS = {3}

# ID's of our path end sprites of sprite.propertie[tile_id]
# for some reason the tile_id is one lower than its representation in the data csv
END_SPRITE_IDS = {3}

# ID's of all path sprites in the data csv
PATH_SPRITE_IDS = {2, 4, 3}
