import pygame
import sys
import os
from constants import *
from shop import MainShop
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
        self.shop = MainShop('right', item_names=item_names, buy_item=self.buy_tower)

        # Enemy list
        self.enemies = []
        self.spawn_enemy()

        # Towers list
        self.archer_towers = []
        self.support_towers = []
        self.towers = []
        self.tower_selected = None

        # Money :
        self.money_font = pygame.font.SysFont("arial", 50)
        self.star_image = pygame.image.load("assets/shop/star.png").convert_alpha()
        self.star_image = pygame.transform.scale_by(self.star_image, 2)
        self.money = 10000

    def spawn_enemy(self):

        self.enemies.append(Enemy())

    def draw_money(self, surface):

        text = self.money_font.render(str(self.money), 1, (255, 255, 255))
        money = pygame.transform.scale(self.star_image, (50, 50))

        start_x = WINDOW_WIDTH - self.star_image.get_width() - 10
        y = 75

        surface.blit(text, (start_x - text.get_width() - 10, y))
        surface.blit(money, (start_x, y))

    def check_money(self, cost):

        if cost <= self.money:
            self.money -= cost
            return True
        else:
            return False

    def buy_tower(self, pos, name, cost):

        if cost <= self.money:
            self.money -= cost

            if name[0:6] == 'archer':
                tower = ArcherTower(pos[0], pos[1], name, self.check_money)
                self.archer_towers.append(tower)
                self.towers.append(tower)
            else:
                tower = Tower(pos[0], pos[1], name, self.check_money)
                self.support_towers.append(tower)
                self.towers.append(tower)
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
                else:
                    for tower in self.towers:
                        tower.check_click(event.pos)

                self.shop.update(event.pos)

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

        # UI:
        self.draw_money(self.screen)

        # Updating screen
        pygame.display.flip()
