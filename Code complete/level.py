from settings import *
from sprites import Sprite, MovingSprite
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
        # Tiles
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

        # objects
        # Loop through objects in the 'Objects' layer of the map
        for obj in tmx_map.get_layer_by_name('Objects'):
            # Check if the current object is the Player start position
            if obj.name == 'Player':
                # Create a new Player object at the specified position (obj.x, obj.y)
                # obj.x and obj.y provide the pixel coordinates for the player's initial location
                # The Player object is added to the all_sprites and collisions_sprites groups
                # This allows the player to be rendered and to interact with other collidable objects
                Player((obj.x, obj.y), self.all_sprites, self.collisions_sprites)

        # Moving objects
        # Loop through objects in the 'Moving Objects' layer of the map
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            # Later on there will be a lots of object so separate it with if statement
            if obj.name == 'helicopter':
                # Becasue the objects is moving left and right
                # So need to figuring out which way is that objects moving
                # Figure out by using the rect that in tiled is wider than it is tall
                if obj.width > obj.height: #horizontal movement
                    move_direction = 'x'
                    # Calculate the starting position of the object:
                    # The x-coordinate is the leftmost point of the object (obj.x).
                    # The y-coordinate is the middle of the object's height (obj.y + obj.height / 2).
                    start_pos = (
                        obj.x,                   # x-coordinate: leftmost point
                        obj.y + obj.height / 2   # y-coordinate: middle of the object's height
                    )
                    
                    # Calculate the ending position of the object:
                    # The x-coordinate is the rightmost point of the object (obj.x + obj.width).
                    # The y-coordinate remains the same as the starting position (obj.y + obj.height / 2).
                    end_pos = (
                        obj.x + obj.width,       # x-coordinate: rightmost point
                        obj.y + obj.height / 2   # y-coordinate: middle of the object's height
                    )
                # Handle verticle movement
                else: 
                    move_direction = 'y'
                    # Calculate the starting position of the object:
                    # The x-coordinate is the leftmost point of the object (obj.x).
                    # The y-coordinate is the middle of the object's height (obj.y + obj.height / 2).
                    start_pos = (
                        obj.x + obj.width / 2,                   # x-coordinate: middle of top point
                        obj.y   # y-coordinate: middle of the object's height
                    )
                    
                    # Calculate the ending position of the object:
                    # The x-coordinate is the rightmost point of the object (obj.x + obj.width).
                    # The y-coordinate remains the same as the starting position (obj.y + obj.height / 2).
                    end_pos = (
                        obj.x + obj.width / 2,   # x-coordinate: middle of top point
                        obj.y + obj.height      # y-coordinate: middle of bottom point
                    )
                # How fast the moving objects gonna be
                # Using the original speed that setting up in tiled which is 100
                speed = obj.properties['speed']
                # Create a MovingObject instance with the calculated start and end positions, speed, and direction, interact with a player
                MovingSprite((self.all_sprites, self.collisions_sprites), start_pos, end_pos, move_direction, speed)

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)