from load_assets import import_folder, import_animations
from data import items_data
import math
import pygame
from shop import VerticalShop
from buttons import Item
import os


class Tower:

    def __init__(self, centerx, centery, name, buy_function, level=0):

        self.check_money = buy_function

        # tower data
        self.name = name
        self.data = items_data[self.name]
        self.upgrade_cost = self.data[3]
        self.max_level = len(self.upgrade_cost)
        self.level = level
        self.placed = False
        self.selected = False

        # size and pos
        self.centerx = centerx
        self.centery = centery
        folder_path = self.data[2]
        self.images = import_folder(folder_path)
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

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        if self.selected:
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

        path = 'assets/towers/archer_top'
        self.animations = import_animations(path)
        self.status = 'front'
        self.archer_image = self.animations[self.status][0]
        self.frame_index = 0
        self.animation_speed = 10
        self.facing_right = True
        self.shooting = False
        self.archer_x = self.x + 50
        self.archer_y = self.y - 15

    def animate(self, dt):

        current_animation = self.animations[self.status]

        if self.shooting:

            # animation loop
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(current_animation):
                self.frame_index = 0

            # get the current animation frame
            image = current_animation[math.floor(self.frame_index)]

        else:

            image = current_animation[0]

        # flipping the image if needed
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False).convert_alpha()

        self.archer_image = image

    def draw(self, surface):

        surface.blit(self.image, (self.x, self.y))
        surface.blit(self.archer_image, (self.archer_x, self.archer_y))

        if self.selected:
            self.upgrade_menu.draw(surface)

    def update_pos(self, pos):

        self.centerx = pos[0]
        self.centery = pos[1]
        self.x = self.centerx - self.width / 2
        self.y = self.centery - self.height / 2
        self.archer_x = self.x + 50
        self.archer_y = self.y - 15
