if __name__ == '__main__':

    import pygame
    import sys

    from game import Game
    from constants import *

    pygame.init()

    #   Creating the game window :
    pygame.display.set_caption('KingdomRush')  # titre de la fenêtre

    # Icon:
    # path = ''
    # win_icon = pygame.image.load(os.path.join(path))
    # pygame.display.set_icon(win_icon)

    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                              pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED, vsync=1)

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
