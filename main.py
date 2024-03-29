import sys
import os
import pygame

from constants import *
from game import Game


def main():
    pygame.init()

    # Music
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join('assets', 'level\\music.mp3'))
    pygame.mixer.music.set_volume(VOLUME)

    #   Creating the game window :
    pygame.display.set_caption('KingdomRush')
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)

    # fps
    clock = pygame.time.Clock()

    game = Game()

    # Main game loop
    running = True
    while running:
        # FPS
        dt = clock.tick(FPS) / 1000  # delta time in seconds

        # get events
        events = pygame.event.get()

        # Main game function
        game.run(events, dt)

    # closing the game
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
