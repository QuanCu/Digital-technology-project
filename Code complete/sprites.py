# Create a class that can actually display stuff into the screen
from pygame.sprite import Group
from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)), groups = None):
        """
        Displaying sprites

        Args:
            pos (tuple): The (x, y) position where the sprite will be placed on the screen.
            surf (pygame.Surface): The Surface where the sprite will be drawn.
            groups (list): A list of groups that this sprite should be added to. 
        """
        super().__init__(groups)
        """
        The superclass (pygame.sprite.Sprite) constructor is called to initialize 
        the sprite and add it to the specified groups.
        """

        # Create a Surface for the sprite.
        self.image = surf
        
        self.image.fill('white')
        
        # Position the sprite on the screen using a rectangle. 
        # The top-left corner of the sprite is set to the given position (pos).
        self.rect = self.image.get_rect(topleft=pos)
        
        # Make a copy of the sprite's rectangle to store its previous position. 
        # This is useful for tracking movement or collisions.
        self.old_rect = self.rect.copy()

# Parameter are inherited from the class Sprite
# Super init use to call the def __init__ of class Sprite
class MovingSprite(Sprite):
    def __init__(self, groups, start_pos, end_pos, move_direction, speed):
        surf = pygame.Surface((200, 50))
        super().__init__(start_pos, surf, groups)
        # Set the sprite's initial position to the center of the rectangle.
        self.rect.center = start_pos
        
        # Store the start and end positions for the sprite's movement.
        self.start_pos = start_pos
        self.end_pos = end_pos
        
        # Store the speed at which the sprite will move.
        self.speed = speed

        # Movement
        if move_direction == 'x':
            self.direction = vector(1,0)
        else:
            self.direction = vector(0,1)

        self.move_direction = move_direction

    def update(self, dt):
        """
        Updating the position

        Args:
            dt (_type_): _description_
        """
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * dt