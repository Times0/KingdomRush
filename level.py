import pygame
import sys
import os
from constants import *
from shop import VerticalShop
from enemy import Enemy
from tower import Tower, ArcherTower


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
        self.shop = VerticalShop('right', item_names=item_names, buy_item=self.buy_item)

        # Enemy list
        self.enemies = []
        self.spawn_enemy()

        # Towers list
        self.archer_towers = []
        self.support_towers = []
        self.tower_selected = None

    def spawn_enemy(self):

        self.enemies.append(Enemy())

    def buy_item(self, pos, name):

        if name[0:6] == 'archer':
            tower = ArcherTower(pos[0], pos[1], name)
            self.archer_towers.append(tower)
        else:
            tower = Tower(pos[0], pos[1], name)
            self.support_towers.append(tower)
        self.tower_selected = tower

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

            elif event.type == pygame.MOUSEMOTION:
                if self.tower_selected is not None:
                    self.tower_selected.update_pos(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.tower_selected is not None:
                    self.tower_selected.place(event.pos)
                    self.tower_selected = None

                self.shop.update(event)

        # Background
        self.screen.blit(self.background, (0, 0))

        # Towers
        for tower in self.support_towers:
            tower.draw(self.screen)
        for tower in self.archer_towers:
            tower.animate(dt)
            tower.draw(self.screen)

        # Enemies
        for enemy in self.enemies:
            enemy.update(dt)
            enemy.draw(self.screen)

        # Shop
        self.shop.draw(self.screen)

        # Updating screen
        pygame.display.flip()
