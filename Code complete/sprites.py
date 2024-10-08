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
        # Setting up the position of the top-bottom of moving object to the top point
        if move_direction==  'x':
            self.rect.midleft = start_pos
        else:
            self.rect.midtop = start_pos 
        # Set the sprite's initial position to the center of the rectangle.
        self.rect.center = start_pos
        
        # Store the start and end positions for the sprite's movement.
        self.start_pos = start_pos
        self.end_pos = end_pos
        
        # Store the speed at which the sprite will move.
        self.speed = speed

        # Movement
        # Naming it so can be use in player.py without getting other elements
        self.moving = True
        # Determine the direction of movement based on the specified axis.
        if move_direction == 'x':
            # If the direction is 'x', the sprite will move horizontally.
            self.direction = vector(1, 0)  # Move right.
        else:
            # If the direction is not 'x', the sprite will move vertically.
            self.direction = vector(0, 1)  # Move down.

        self.move_direction = move_direction
    
    def check_border(self):
        # Check if the sprite has reached the border in the horizontal direction (left to right movement).
        if self.move_direction == 'x':
            # If the sprite's right edge has reached or exceeded the end position's x-coordinate
            # and the sprite is currently moving to the right (direction.x == 1).
            if self.rect.right >= self.end_pos[0] and self.direction.x == 1:
                # Reverse the horizontal direction of movement (change from moving right to moving left).
                self.direction.x = -1
                # Adjust the sprite's right edge to exactly match the end position's x-coordinate.
                self.rect.right = self.end_pos[0]
            if self.rect.left <= self.start_pos[0] and self.direction.x == -1:
                # Reverse the horizontal direction of movement (change from moving right to moving left).
                self.direction.x = 1
                # Adjust the sprite's right edge to exactly match the end position's x-coordinate.
                self.rect.left = self.start_pos[0]
        else:
            # If the sprite's right edge has reached or exceeded the end position's x-coordinate
            # and the sprite is currently moving to the right (direction.x == 1).
            if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1:
                # Reverse the horizontal direction of movement (change from moving right to moving left).
                self.direction.y = -1
                # Adjust the sprite's right edge to exactly match the end position's x-coordinate.
                self.rect.bottom = self.end_pos[1]
            if self.rect.top <= self.start_pos[1] and self.direction.y == -1:
                # Reverse the horizontal direction of movement (change from moving right to moving left).
                self.direction.y = 1
                # Adjust the sprite's right edge to exactly match the end position's x-coordinate.
                self.rect.top = self.start_pos[1]



    def update(self, dt):
        """
        Updating the position

        Args:
            dt (_type_): The time that making the game looks smoother
        """
        # Save the current position of the sprite's rectangle for future reference.
        self.old_rect = self.rect.copy()
        
        # Update the sprite's position by moving it in the specified direction.
        # The position is adjusted based on the direction vector, speed, and delta time.
        self.rect.topleft += self.direction * self.speed * dt
        self.check_border()