from pygame.sprite import Group
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        # Size of a player
        self.image = pygame.Surface((64,64))
        # Leaving player color blue to see what happen
        self.image.fill('blue')

        # rects
        self.rect = self.image.get_frect(topleft = pos)
        # Main rectangle, show where the player will be draw
        self.old_rect = self.rect.copy()
        # Movement
        # Vector is automatically at 0,0 because the player
        # Is only move when the button is being pressed
        self.direction = vector()
        self.speed = 200
        # Gravity
        self.gravity = 800
        # Jumping
        self.jump = False
        self.jump_height = 800

        #Collision
        self.collision_sprites = collision_sprites
        self.on_surface = {'floor': False}


    def input(self):
        # Locol variable 
        # Used to get all of the keys in the keyboard
        keys = pygame.key.get_pressed()
        # On every frame of the game,
        # the input vector starts at the position 0,0
        # After doing this, 
        # can update the player depending on direction of moving
        input_vector = vector(0,0)
        # If the player is moving right
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        # If the player is moving left
        elif keys[pygame.K_LEFT]:
            input_vector.x -= 1

        # Changing the direction than normalize it to 
        # Make sure the vector is the same length
        # And ensuring that the speed is always the same
        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x
            
        # Check for jumping
        if keys[pygame.K_SPACE]:
            self.jump = True

    def move(self, dt):
        """
        Move the player based on the input
        """
        # Taking the current position of the player and incresing it by a speed in a certain direction
        #Doing the horizontal collision
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        #Doing the vertical collision
        # Apply gravity to the player's vertical direction.
        # The gravity value is split into two increments to smoothly increase the downward velocity.
        # This helps simulate a more natural acceleration due to gravity over time.
        # The formula `gravity / 2 * dt` adjusts the velocity based on time elapsed (`dt`),
        # ensuring consistent behavior regardless of the frame rate.
        self.direction.y += self.gravity / 2 * dt

        # Update the player's vertical position.
        # The current vertical position (`self.rect.y`) is adjusted by the vertical velocity (`self.direction.y`).
        # Multiplying by `dt` ensures that the movement is time-dependent,
        # making it frame-rate independent (e.g., if dt is small, the movement is small).
        self.rect.y += self.direction.y * dt

        # Apply the second half of the gravity to the vertical direction.
        # This additional gravity increment further increases the downward velocity,
        # simulating continuous acceleration (falling faster over time).
        # By splitting the gravity application into two parts, the fall speed increases more smoothly.
        self.direction.y += self.gravity / 2 * dt

        # Perform vertical collision detection and response.
        # The `collision` method is called with the argument 'verticle' (should be 'vertical').
        # This checks if the player's updated vertical position results in a collision with any
        # objects or tiles in the environment (e.g., the ground or platforms).
        # If a collision is detected, the player's position will be adjusted to prevent them
        # from moving through the object, effectively stopping the player from falling further.
        self.collision('verticle')

        # Checking for jumping
        # If the player is on the surface, aloud it to jump
        if self.jump:
            if self.on_surface['floor']:
                self.direction.y = -self.jump_height
                self.jump = False
        
    def check_contact(self):
        """
        Checking if the player is having contact with the floor
        """
        # Creating 3 rect in 3 side of the player,
        # If the rect of the sprites is contact with the rect
        # Of the player, player will know which side have contact
        floor_rect = pygame.Rect((self.rect.bottomleft),(self.rect.width,2))
        # List of colliding objects that could be colliding with
        collide_rects = [sprite.rect for sprite in self.collision_sprites]
        # Check if the player's collision rectangle is touching any of the floor rectangles
        if floor_rect.collidelist(collide_rects) >= 0:
            self.on_surface['floor'] = True
        else:
            self.on_surface['floor'] = False

    def collision(self,axis):
        """
        Checking if collision

        Args:
            axis (str): This axis could be horizontal or verticle.
        """
        # Look at all of the sprites inside of collision
        # Cheking if there is an overlap
        for sprite in self.collision_sprites:
            #Checking collision between the Sprite and the rectangle of the player
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # Checking where that over lap come from whether left or right
                    # Left collision
                    # Checking if the left side of the player against the right side of
                    # The sprites. As it colliding, the left side of the player
                    # Is always smaller or equal than the right side of the sprites
                    # 2nd condition is checking the last position of the player if the left side 
                    # of the player was greater than the right side of the obstacle
                    # After that setting the position of the player to stay in that
                    # position
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    # Right collision
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                else: # Verticle collision
                    if self.rect.top <= sprite.rect.bottom and int(self.old_rect.top) >= int(sprite.old_rect.bottom):
                        self.rect.top = sprite.rect.bottom
                    elif self.rect.bottom >= sprite.rect.top and int(self.old_rect.bottom) <= int(sprite.old_rect.top):
                        self.rect.bottom = sprite.rect.top
                    # Setting if having any verticle collision, setting the self.direction equal to 0
                    self.direction.y = 0

    def update(self, dt):
        """
        Call all of the update methods inside of the sprite
        """
        # Self.rect have the current position while 
        # Old.rect have the old position
        # Storing the current position of the rectangle
        # Inside of old rectangle
        # So then when doing the movement, getting a new position instead of
        # current position
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)
        self.check_contact()