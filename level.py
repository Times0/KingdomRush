import pygame
import sys
import os
from constants import *
from shop import VerticalShop
from enemy import Enemy


class Level:

    def __init__(self, show_menu):

        self.screen = pygame.display.get_surface()
        self.show_menu = show_menu

        # Import background image
        bg_path = 'assets/level/bg.png'
        self.background = pygame.image.load(os.path.join(bg_path))
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Import different items :
        item_names = ['archers lvl 1', 'archers lvl 2', 'increase damage', 'increase range']

        # creating the menu with each item
        self.shop = VerticalShop('right', item_names=item_names)

        # Enemy list
        self.enemies = []
        self.spawn_enemy()

    def spawn_enemy(self):

        self.enemies.append(Enemy())

    def run(self, events, dt):

        # event handler
        for event in events:

            # quitting game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:

                # return to menu with escape key
                if event.key == pygame.K_ESCAPE:
                    self.show_menu()

        # Background
        self.screen.blit(self.background, (0, 0))

        # Shop
        self.shop.draw(self.screen)

        # Enemies
        for enemy in self.enemies:
            enemy.update(dt)
            enemy.draw(self.screen)

        # Updating screen
        pygame.display.flip()
