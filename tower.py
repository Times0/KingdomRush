import math
import os

import pygame

from assets import archer_animations, arrow_img
from buttons import Item
from data import items_data
from shop import VerticalShop


class Tower:

    def __init__(self, centerx, centery, name, buy_function, level=0):

        self.check_money = buy_function

        # tower data
        self.name = name
        self.data = items_data[self.name]
        self.upgrade_cost = [1500, 2500]
        self.max_level = len(self.upgrade_cost)
        self.level = level
        self.ranges = [200, 300, 400]
        self.range = self.ranges[self.level]
        self.placed = False
        self.selected = False
        self.placement_range = 200
        self.placement_allowed = True

        # size and pos
        self.centerx = centerx
        self.centery = centery
        self.images = self.data['images']
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
        self.range = self.ranges[self.level]

    def draw(self, surface, draw_range=True, tower_selected=None):

        if tower_selected is not None:
            self.draw_placement_indicator(surface)

        surface.blit(self.image, (self.x, self.y))

        if draw_range and (not self.placed or self.selected):
            self.draw_range(surface)

        if self.selected and self.level != self.max_level:
            self.upgrade_menu.draw(surface)

    def draw_placement_indicator(self, surface):

        if self.placement_allowed:
            color = (0, 0, 255, 100)
        else:
            color = (255, 0, 0, 100)

        radius = self.placement_range / 2
        surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(surf, color, (radius, radius), radius)
        # pygame.draw.circle(surf, COLOR_TURRET_radius_CONTOUR, (radius, radius), radius, 2)
        surface.blit(surf, (self.centerx - radius, self.centery - radius))

    def draw_range(self, surface):
        surf = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(surf, (*COLOR_TURRET_RANGE, 100), (self.range, self.range), self.range)
        pygame.draw.circle(surf, COLOR_TURRET_RANGE_CONTOUR, (self.range, self.range), self.range, 2)
        surface.blit(surf, (self.centerx - self.range, self.centery - self.range))

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
            elif self.level != self.max_level:
                self.upgrade_menu.update(event_pos)
        else:
            self.selected = False

    def collide(self, other_tower):
        x2 = other_tower.centerx
        y2 = other_tower.centery

        dis = math.sqrt((x2 - self.centerx) ** 2 + (y2 - self.centery) ** 2)
        if dis >= self.placement_range:
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
        self.attack_speed = 10
        self.animation_speed = self.attack_speed
        self.facing_right = True
        self.shooting = False
        self.arrows = []
        self.archer_x = self.x + 50
        self.archer_y = self.y - 15
        self.arrow_x = self.archer_x + self.archer_image.get_width()

        self.ranges = [300, 400, 500]
        self.range = self.ranges[self.level]
        self.damages = [1, 2, 4]
        self.damage = self.damages[self.level]

    def upgrade(self):
        super().upgrade()
        self.damage = self.damages[self.level]

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

    def update_arrows(self, dt):
        for arrow in self.arrows:
            arrow.update(dt)
            if arrow.check_target():
                if arrow.target.status != 'die':
                    arrow.target.hit(arrow.damage)
                self.arrows.remove(arrow)

    def draw(self, surface, draw_range=True, tower_selected=None):

        if tower_selected is not None:
            super().draw_placement_indicator(surface)

        surface.blit(self.image, (self.x, self.y))
        surface.blit(self.archer_image, (self.archer_x, self.archer_y))

        for arrow in self.arrows:
            arrow.draw(surface)

        if draw_range and (not self.placed or self.selected):
            super().draw_range(surface)

        if self.selected and self.level != self.max_level:
            self.upgrade_menu.draw(surface)

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
                    (self.centerx - x) ** 2 + (self.centery - y) ** 2)

                if dis < self.range and dis < closest_enemy_dis:
                    closest_enemy = enemy
                    closest_enemy_dis = dis

        if closest_enemy is not None:

            # Attacking the closest enemy
            # Changing the archers direction depending on the enemy position relative to the tower
            if closest_enemy.x > self.centerx and not self.facing_right:
                self.facing_right = True
            elif self.facing_right and closest_enemy.x < self.centerx:
                self.facing_right = False

            if not self.shooting:
                self.shooting = True

                self.arrows.append(Arrow(self.archer_center_x, self.archer_center_y, closest_enemy, self.damage))

    def update_pos(self, pos):

        self.centerx = pos[0]
        self.centery = pos[1]
        self.x = self.centerx - self.width / 2
        self.y = self.centery - self.height / 2
        self.archer_x = self.x + 50
        self.archer_y = self.y - 15
        self.archer_center_x = self.archer_x + self.archer_image.get_width() / 2
        self.archer_center_y = self.archer_y + self.archer_image.get_height() / 2


class SupportTower(Tower):
    def __init__(self, centerx, centery, name, buy_function, level=0):
        super().__init__(centerx, centery, name, buy_function, level=level)
        self.range = 400
        self.effect = [1.2, 1.4]
        self.affected_towers = list()

    def get_affected_towers(self, towers):

        affected_towers = []
        for tower in towers:
            x = tower.centerx
            y = tower.centery

            dis = math.sqrt((self.centerx - x) ** 2 + (self.centery - y) ** 2)

            if dis <= self.range:
                affected_towers.append(tower)

        self.affected_towers = affected_towers


class RangeTower(SupportTower):

    def __init__(self, centerx, centery, name, buy_function, level=0):
        super().__init__(centerx, centery, name, buy_function, level=level)
        self.upgrade_cost = [2000]
        self.upgrade_menu.items[0].change_cost(self.upgrade_cost[self.level])
        self.max_level = len(self.upgrade_cost)
        self.ranges = [250, 350]
        self.range = self.ranges[self.level]
        self.effect = [1.2, 1.4]

    def support(self):
        effect = self.effect[self.level]
        for tower in self.affected_towers:
            original_range = tower.ranges[tower.level]
            tower.range = round(original_range * effect)


class SpeedTower(SupportTower):

    def __init__(self, centerx, centery, name, buy_function, level=0):
        super().__init__(centerx, centery, name, buy_function, level=level)
        self.upgrade_cost = [3000]
        self.upgrade_menu.items[0].change_cost(self.upgrade_cost[self.level])
        self.max_level = len(self.upgrade_cost)
        self.ranges = [250, 350]
        self.range = self.ranges[self.level]
        self.effect = [1.2, 2]

    def support(self):
        effect = self.effect[self.level]
        for tower in self.affected_towers:
            original_speed = tower.attack_speed
            tower.animation_speed = original_speed * effect


class ArcherTowerLong(ArcherTower):
    def __init__(self, centerx, centery, name, buy_function, level=0):
        super().__init__(centerx, centery, name, buy_function, level=level)
        self.upgrade_cost = [1000, 2000]
        self.upgrade_menu.items[0].change_cost(self.upgrade_cost[self.level])
        self.max_level = len(self.upgrade_cost)
        self.ranges = [400, 500, 600]
        self.range = self.ranges[self.level]
        self.damages = [1, 3, 6]
        self.damage = self.damages[self.level]


class ArcherTowerShort(ArcherTower):
    def __init__(self, centerx, centery, name, buy_function, level=0):
        super().__init__(centerx, centery, name, buy_function, level=level)
        self.upgrade_cost = [1000, 2000]
        self.upgrade_menu.items[0].change_cost(self.upgrade_cost[self.level])
        self.max_level = len(self.upgrade_cost)
        self.ranges = [250, 350, 450]
        self.range = self.ranges[self.level]
        self.damages = [2, 4, 8]
        self.damage = self.damages[self.level]


class Arrow:

    def __init__(self, centerx, centery, enemy, damage):
        self.centerx = centerx
        self.centery = centery
        self.target = enemy
        self.damage = damage
        self.image = arrow_img
        self.x = self.centerx - self.image.get_width() / 2
        self.y = self.centery - self.image.get_height() / 2
        self.original_dir = (1, 0)
        self.rotated_image = self.image
        self.speed = 1000

    def rotate(self, angle):
        """rotate the image while keeping its center and size"""
        rotated_image = pygame.transform.rotate(self.image, angle)
        self.rotated_image = rotated_image

    def update_direction(self):
        x1, y1 = self.centerx, self.centery
        x2, y2 = self.target.x, self.target.y

        dirn = ((x2 - x1) * 2, (y2 - y1) * 2)
        length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
        dirn = (dirn[0] / length, dirn[1] / length)

        self.direction = dirn

    def get_angle(self):

        (x1, y1) = self.original_dir
        (x2, y2) = self.direction

        v1_theta = math.atan2(x1, y1)
        v2_theta = math.atan2(x2, y2)

        r = (v2_theta - v1_theta) * (180.0 / math.pi)

        if r < 0:
            r += 360.0

        return r

    def move(self, dt):
        """Move enemy"""

        dirn = self.direction
        move_x, move_y = dirn[0] * self.speed * dt, dirn[1] * self.speed * dt

        self.centerx += move_x
        self.centery += move_y

    def check_target(self):

        x = self.target.x
        y = self.target.y

        dis = math.sqrt((self.centerx - x) ** 2 + (self.centery - y) ** 2)

        if dis <= 50:
            return True

    def update(self, dt):
        self.update_direction()
        angle = self.get_angle()
        self.rotate(angle)
        self.move(dt)

    def draw(self, surface):
        self.x = self.centerx - self.rotated_image.get_width()
        self.y = self.centery - self.rotated_image.get_height()
        surface.blit(self.rotated_image, (self.x, self.y))


COLOR_TURRET_RANGE = (123, 162, 115)
COLOR_TURRET_RANGE_CONTOUR = (53, 73, 48)
