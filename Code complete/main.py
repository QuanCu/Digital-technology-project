from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join

# This class is going to run the basic logic
class Game:
    def __init__(self):
        pygame.init()
        # Passing through the width and height of the window
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        #Name of the game
        pygame.display.set_caption("Adventure 1")
        # Clock object to control the frame rate
        self.clock = pygame.time.Clock()

        # Creating the dictionary that store all the map file
        # Passing through the path to tmx file in here that will later on
        # Passing it through self.current_stage to draw
        #Data\Second level.tmx 
        self.tmx_maps = {0: load_pygame(join('Data', 'Second Level.tmx'))}
        self.current_stage = Level(self.tmx_maps[0])

    def run(self):
        """
        Creating the game loop
        """
        run = True
        while run:
            # Get the number in second
            dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                #Check if the user quit the game
                if event.type == pygame.QUIT:
                    run = False
                    break

            self.current_stage.run(dt)
            pygame.display.update()

# Make sure that don't run anything accidentally 
if __name__ == '__main__':
    game = Game()
    game.run()