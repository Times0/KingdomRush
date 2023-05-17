import os
import sys

import pygame

from constants import *
from data import waves, wave_enemies
from enemy import Enemy, Ogre
from shop import MainShop
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

        # Enemies
        self.enemies = []
        self.wave_count = 0
        self.current_wave = None
        self.SPAWN_ENEMY = pygame.event.custom_type()
        self.time_between_enemies = 2000
        self.last_enemy_time = -self.time_between_enemies

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

        self.path_debug = []

    def start_next_wave(self):
        self.current_wave = waves[self.wave_count]

    def spawn_enemy(self, enemy_type='ogre'):
        if enemy_type == 'ogre':
            enemy = Ogre()
        else:
            enemy = Enemy()
        self.enemies.append(enemy)

    def spawn_next_enemy(self):

        if sum(self.current_wave) == 0:
            if len(self.enemies) == 0:
                self.wave_count += 1
                self.current_wave = None
        else:
            for enemy_index, nb_enemy in enumerate(self.current_wave):
                if nb_enemy != 0:
                    enemy_type = wave_enemies[enemy_index]
                    self.spawn_enemy(enemy_type)
                    self.last_enemy_time = pygame.time.get_ticks()
                    self.current_wave[enemy_index] -= 1
                    break

    def draw_money(self, surface):

        text = self.money_font.render(str(self.money), True, (255, 255, 255))
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
                    self.tower_selected = None
                    self.show_menu()

                # spawn enemy with space key
                if event.key == pygame.K_SPACE:
                    self.start_next_wave()

            elif event.type == pygame.MOUSEMOTION:
                if self.tower_selected is not None:
                    self.tower_selected.update_pos(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.path_debug.append(event.pos)
                # print(self.path_debug)
                if self.tower_selected is not None:
                    self.tower_selected.place(event.pos)
                    self.tower_selected = None
                else:
                    for tower in self.towers:
                        tower.check_click(event.pos)

                self.shop.update(event.pos)

        # Spawning enemies:
        if self.current_wave is not None:
            if pygame.time.get_ticks() - self.last_enemy_time > self.time_between_enemies:
                self.spawn_next_enemy()

        # Background
        self.screen.blit(self.background, (0, 0))

        # Towers
        for tower in self.support_towers:
            tower.draw(self.screen)
        for tower in self.archer_towers:
            if tower.placed:
                tower.attack(self.enemies)
                tower.animate(dt)
            tower.draw(self.screen)

        # Enemies
        for index, enemy in enumerate(self.enemies):
            enemy.update(dt)
            if enemy.dead:
                if index + 1 < len(self.enemies):
                    self.enemies[index + 1].update(dt)
                    self.enemies[index + 1].draw(self.screen)
                self.enemies.remove(enemy)
                self.money += enemy.money

            else:
                enemy.draw(self.screen)

        # Shop
        self.shop.draw(self.screen)

        # UI:
        self.draw_money(self.screen)

        # Updating screen
        pygame.display.flip()
