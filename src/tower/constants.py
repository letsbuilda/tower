"""Variables that are needed in multiple files and don't change."""

# Map
MAP_WIDTH = 24
MAP_HEIGHT = 15

# Screen
SCREEN_WIDTH = MAP_WIDTH * 64
SCREEN_HEIGHT = MAP_HEIGHT * 64
SCREEN_TITLE = "Platformer"

# ID's of our path start sprites in the data csv
START_SPRITE_IDS = {3}

# ID's of our path end sprites in the data csv
END_SPRITE_IDS = {4}

# ID's of all path sprites in the data csv
PATH_SPRITE_IDS = {2, 4, 3}
