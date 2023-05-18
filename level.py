import os
import sys

import pygame
from data import items_data
from constants import *
from data import waves, wave_enemies
from shop import MainShop
from enemy import Enemy, Ogre
from tower import ArcherTowerLong, ArcherTowerShort, RangeTower, SpeedTower
from buttons import ToggleButton
from assets import pause_img, start_img, sound_on, sound_off


class Level:

    def __init__(self, show_menu):

        self.screen = pygame.display.get_surface()
        self.show_menu = show_menu

        self.paused = False
        self.pause_time = 0

        # Import background image
        bg_path = 'assets/level/bg.png'
        self.background = pygame.image.load(os.path.join(bg_path))
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Import different items :
        item_names = list(items_data.keys())
        item_names.remove('path')

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
        self.star_image = pygame.image.load("assets/ui/star.png").convert_alpha()
        self.star_image = pygame.transform.scale(self.star_image, (50, 50))
        self.money = 10000

        # Health
        self.health_font = self.money_font
        self.heart_image = pygame.image.load("assets/ui/heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (50, 50))
        self.health = 10

        # UI:
        self.buttons = []
        # Play/pause button:
        offset = 10
        x = offset
        y = WINDOW_HEIGHT - pause_img.get_height() - offset
        self.pause_btn = ToggleButton([start_img, pause_img], (x, y), [self.unpause, self.pause])
        self.buttons.append(self.pause_btn)

        # Sound On/off button:
        offset = 10
        x = offset + start_img.get_width() + offset
        y = WINDOW_HEIGHT - pause_img.get_height() - offset
        self.music_btn = ToggleButton([sound_on, sound_off], (x, y),
                                      [pygame.mixer.music.pause, pygame.mixer.music.unpause])
        self.buttons.append(self.music_btn)

        self.path_debug = []

    def start_next_wave(self):

        self.current_wave = waves[self.wave_count]

    def pause(self):

        self.paused = True
        self.pause_time = pygame.time.get_ticks()

    def unpause(self):
        if self.current_wave is None:
            self.start_next_wave()
        else:
            if self.paused:
                self.last_enemy_time = pygame.time.get_ticks() - self.pause_time + self.last_enemy_time
        self.paused = False

    def spawn_enemy(self, enemy_type='ogre'):

        if enemy_type == 'ogre':
            enemy = Ogre()
        else:
            enemy = Enemy()
        self.enemies.append(enemy)

    def check_death(self):

        if self.health <= 0:
            self.show_menu()

    def spawn_next_enemy(self):

        if sum(self.current_wave) == 0:
            if len(self.enemies) == 0:
                self.wave_count += 1
                self.current_wave = None
                self.paused = True
                self.pause_btn.toggle()
        else:
            for enemy_index, nb_enemy in enumerate(self.current_wave):
                if nb_enemy != 0:
                    enemy_type = wave_enemies[enemy_index]
                    self.spawn_enemy(enemy_type)
                    self.last_enemy_time = pygame.time.get_ticks()
                    self.current_wave[enemy_index] -= 1
                    break

    def draw_health(self, surface):

        text = self.health_font.render(str(self.health), True, (255, 255, 255))

        start_x = WINDOW_WIDTH - self.heart_image.get_width() - 10
        y = 75

        surface.blit(text, (start_x - text.get_width() - 10, y))
        surface.blit(self.heart_image, (start_x, y))

    def draw_money(self, surface):

        text = self.money_font.render(str(self.money), True, (255, 255, 255))

        start_x = WINDOW_WIDTH - self.star_image.get_width() - 10
        y = 10

        surface.blit(text, (start_x - text.get_width() - 10, y))
        surface.blit(self.star_image, (start_x, y))

    def check_money(self, cost):

        if cost <= self.money:
            self.money -= cost
            return True
        else:
            return False

    def buy_tower(self, pos, name, cost):

        if cost <= self.money:
            self.money -= cost

            if name == 'archers long':
                tower = ArcherTowerLong(pos[0], pos[1], name, self.check_money)
                self.archer_towers.append(tower)
            elif name == 'archers short':
                tower = ArcherTowerShort(pos[0], pos[1], name, self.check_money)
                self.archer_towers.append(tower)
            elif name == 'increase speed':
                tower = SpeedTower(pos[0], pos[1], name, self.check_money)
                self.support_towers.append(tower)
            elif name == 'increase range':
                tower = RangeTower(pos[0], pos[1], name, self.check_money)
                self.support_towers.append(tower)
            else:
                text = 'name: \'' + name + '\' is not a valid tower name'
                raise Exception(text)

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
                self.path_debug.append(event.pos)
                # print(self.path_debug)

                for button in self.buttons:
                    if button.on_mouse_clicked(event.pos):
                        # button clicked
                        if button.on_click:
                            button.on_click()

                if self.tower_selected is not None:
                    self.tower_selected.place(event.pos)
                    self.tower_selected = None
                else:
                    for tower in self.towers:
                        tower.check_click(event.pos)

                self.shop.update(event.pos)

        # Spawning enemies:
        if self.current_wave is not None:
            if not self.paused:
                if pygame.time.get_ticks() - self.last_enemy_time > self.time_between_enemies:
                    self.spawn_next_enemy()

        # Background
        self.screen.blit(self.background, (0, 0))

        # Towers
        for tower in self.support_towers:
            tower.get_affected_towers(self.archer_towers)
            tower.support()
            tower.draw(self.screen)
        for tower in self.archer_towers:
            if tower.placed:
                if not self.paused:
                    tower.attack(self.enemies)
                    tower.animate(dt)
            tower.draw(self.screen)

        # Enemies
        for index, enemy in enumerate(self.enemies):
            if not self.paused:
                enemy.update(dt)
            if enemy.dead or enemy.off_screen:
                if index + 1 < len(self.enemies):
                    if not self.paused:
                        self.enemies[index + 1].update(dt)
                    self.enemies[index + 1].draw(self.screen)
                self.enemies.remove(enemy)
                if enemy.dead:
                    self.money += enemy.money
                elif enemy.off_screen:
                    self.health -= 1
                    self.check_death()

            else:
                enemy.draw(self.screen)

        # Shop
        self.shop.draw(self.screen)

        # UI:
        self.draw_money(self.screen)
        self.draw_health(self.screen)
        for button in self.buttons:
            button.draw(self.screen)

        # Updating screen
        pygame.display.flip()
