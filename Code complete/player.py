from pygame.sprite import Group
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((64,64))
        self.image.fill('blue')
        self.rect = self.image.get_frect(topleft = pos)