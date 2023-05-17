import math
import os

import pygame

from assets import archer_animations
from buttons import Item
from data import towers_data
from shop import VerticalShop


class Tower:

    def __init__(self, centerx, centery, name, buy_function, level=0):

        self.check_money = buy_function

        # tower data
        self.name = name
        self.data = towers_data[self.name]
        self.upgrade_cost = self.data[3]
        self.max_level = len(self.upgrade_cost)
        self.level = level
        self.placed = False
        self.selected = False

        # size and pos
        self.centerx = centerx
        self.centery = centery
        self.images = self.data[2]
        self.image = self.images[self.level]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = self.centerx - self.width / 2
        self.y = self.centery - self.height / 2

        image = pygame.image.load(os.path.join('assets\\shop', 'upgrade.png')).convert_alpha()
        image = pygame.transform.scale_by(image, .5)
        cost = self.upgrade_cost[self.level]
        on_click = self.upgrade
        item = Item(image, (0, 10), 150, name, cost, on_click=on_click)
        self.upgrade_menu = VerticalShop([item], width=150)

    def upgrade(self):

        if self.level < self.max_level:
            cost = self.upgrade_cost[self.level]
            if self.check_money(cost):
                self.level += 1
                if self.level != self.max_level:
                    new_cost = self.upgrade_cost[self.level]
                    self.upgrade_menu.items[0].change_cost(new_cost)
        self.image = self.images[self.level]
        self.selected = False

    def draw(self, surface, draw_range=False):
        surface.blit(self.image, (self.x, self.y))
        if self.selected and self.level != self.max_level:
            self.upgrade_menu.draw(surface)

    def update_pos(self, pos):
        self.centerx = pos[0]
        self.centery = pos[1]
        self.x = self.centerx - self.width / 2
        self.y = self.centery - self.height / 2

    def check_click(self, event_pos):
        # check if tower is clicked

        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if rect.collidepoint(event_pos):
            if not self.selected:
                self.selected = True
            else:
                self.upgrade_menu.update(event_pos)
        else:
            self.selected = False

    def collide(self, other_tower):
        x2 = other_tower.x
        y2 = other_tower.y

        dis = math.sqrt((x2 - self.x) ** 2 + (y2 - self.y) ** 2)
        if dis >= 100:
            return False
        else:
            return True

    def place(self, pos):
        self.placed = True
        self.centerx = pos[0]
        self.centery = pos[1]
        self.x = self.centerx - self.width / 2
        self.y = self.centery - self.height / 2
        self.upgrade_menu.x = self.centerx - self.upgrade_menu.width / 2
        self.upgrade_menu.y = self.centery - self.upgrade_menu.height / 2


class ArcherTower(Tower):

    def __init__(self, centerx, centery, name, buy_function, level=0):
        super().__init__(centerx, centery, name, buy_function, level=level)

        self.animations = archer_animations
        self.status = 'front'
        self.archer_image = self.animations[self.status][0]
        self.frame_index = 0
        self.animation_speed = 10
        self.facing_right = True
        self.shooting = False
        self.archer_x = self.x + 50
        self.archer_y = self.y - 15

        self.range = 400
        self.damage = 1

    def animate(self, dt):

        current_animation = self.animations[self.status]

        if self.shooting:

            # animation loop
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(current_animation):
                self.frame_index = 0
                self.shooting = False

            # get the current animation frame
            image = current_animation[math.floor(self.frame_index)]

        else:

            image = current_animation[0]

        # flipping the image if needed
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False).convert_alpha()

        self.archer_image = image

    def draw(self, surface, draw_range=True):

        surface.blit(self.image, (self.x, self.y))
        surface.blit(self.archer_image, (self.archer_x, self.archer_y))

        if self.selected and self.level != self.max_level:
            self.upgrade_menu.draw(surface)

        if draw_range and not self.placed:
            surf = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA, 32)
            pygame.draw.circle(surf, (220, 220, 220, 50), (self.range, self.range), self.range)
            pygame.draw.circle(surf, (220, 220, 220), (self.range, self.range), self.range, 2)
            surface.blit(surf, (self.centerx - self.range, self.centery - self.range))

    def attack(self, enemies):
        """
        attacks the closest enemy
        updates the archers facing direction based on the enemy location
        """

        # Finding the closest enemy to the tower
        closest_enemy = None
        closest_enemy_dis = self.range
        for enemy in enemies:

            if enemy.status != 'die':
                x = enemy.x
                y = enemy.y

                dis = math.sqrt(
                    (self.x - x) ** 2 + (self.y - y) ** 2)

                if dis < self.range and dis < closest_enemy_dis:
                    closest_enemy = enemy
                    closest_enemy_dis = dis

        if closest_enemy is not None:

            # Attacking the closest enemy
            if not self.shooting:
                self.shooting = True
                closest_enemy.hit(self.damage)

            # Changing the archers direction depending on the enemy position relative to the tower
            if closest_enemy.x > self.x and not self.facing_right:
                self.facing_right = True
            elif self.facing_right and closest_enemy.x < self.x:
                self.facing_right = False

    def update_pos(self, pos):

        self.centerx = pos[0]
        self.centery = pos[1]
        self.x = self.centerx - self.width / 2
        self.y = self.centery - self.height / 2
        self.archer_x = self.x + 50
        self.archer_y = self.y - 15
