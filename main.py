if __name__ == '__main__':

    import pygame
    import sys

    from game import Game
    from constants import *

    pygame.init()

    #   Creating the game window :
    pygame.display.set_caption('KingdomRush')
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)

    # fps
    clock = pygame.time.Clock()

    game = Game()

    # Main game loop
    running = True
    while running:
        # get events
        events = pygame.event.get()

        # Main game function
        game.run(events)

        # FPS
        clock.tick(FPS)

    # closing the game
    pygame.quit()
    sys.exit()
