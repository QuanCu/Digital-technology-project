# Create a class that can actually display stuff into the screen
from pygame.sprite import Group
from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        """
        Displaying sprites

        Args:
            pos (_type_): position that we want to passing the sprite on
            surf (_type_): Surface that putting the sprite in
            groups (_type_): putting the sprites in groups and the groups are displaying
        """
        super().__init__(groups)
        """
        Assigning sprites into groups when creating it
        """
        # The image is what wnat to display
        # TIle size is 64 as in the setting file
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        # Just to see if using the right size
        self.image.fill('white')
        #Positioning the sprite
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
