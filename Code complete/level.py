from settings import *
from sprites import Sprite
from player import Player

class Level:
    def __init__(self, tmx_map):
        # Also can draw on the surface that create in main.py 
        self.display_surface = pygame.display.get_surface()
        # Groups
        #Every single sprite that create 
        # Will be inside of this group
        self.all_sprites = pygame.sprite.Group()
        # Handle collision
        # Contain all of the colliable sprites
        self.collisions_sprites = pygame.sprite.Group()
        # Call the setup method to initialize the map
        self.setup(tmx_map)

    def setup(self, tmx_map):
        """


        Args:
            tmx_map (_type_): _description_
        """
        # Target one specific layer inside the map tield
        # Getting the Terrain layer first.
        # Loop through to getting the x, y, surface position
        # Currently x and y is grip position not pixel position so times by 
        # TILE_SIZE to convert into pixel postition
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            # Create a new Sprite object for each tile in the 'Terrain' layer
            # (x, y) gives the position on the map, and surf is the surface image for the tile
            # The new Sprite is added to the all_sprites group for further handling and rendering
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, (self.all_sprites, self.collisions_sprites))

        # Loop through objects in the 'Objects' layer of the map
        for obj in tmx_map.get_layer_by_name('Objects'):
            # Check if the current object is the Player start position
            if obj.name == 'Player':
                # Create a new Player object at the specified position (obj.x, obj.y)
                # obj.x and obj.y provide the pixel coordinates for the player's initial location
                # The Player object is added to the all_sprites and collisions_sprites groups
                # This allows the player to be rendered and to interact with other collidable objects
                Player((obj.x, obj.y), self.all_sprites, self.collisions_sprites)

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)