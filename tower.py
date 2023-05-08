from load_assets import import_folder, import_animations
from data import items_data
import math
import pygame


class Tower:

    def __init__(self, centerx, centery, name, level=0):
        # tower data
        self.name = name
        self.data = items_data[self.name]
        self.upgrade_cost = self.data[3]
        self.max_level = len(self.upgrade_cost)
        self.level = level
        self.placed = False

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

    def upgrade(self):

        self.level += 1
        self.image = self.images[self.level]

    def draw(self, surface):

        surface.blit(self.image, (self.x, self.y))

    def update_pos(self, pos):
        self.centerx = pos[0]
        self.centery = pos[1]
        self.x = self.centerx - self.width / 2
        self.y = self.centery - self.height / 2

    def place(self, pos):
        self.placed = True
        self.centerx = pos[0]
        self.centery = pos[1]
        self.x = self.centerx - self.width / 2
        self.y = self.centery - self.height / 2


class ArcherTower(Tower):

    def __init__(self, centerx, centery, name, level=0):
        super().__init__(centerx, centery, name, level=level)

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

    def update_pos(self, pos):

        self.centerx = pos[0]
        self.centery = pos[1]
        self.x = self.centerx - self.width / 2
        self.y = self.centery - self.height / 2
        self.archer_x = self.x + 50
        self.archer_y = self.y - 15
