import pygame
import os
from load_assets import import_animations
import math


class Enemy:
    def __init__(self, folder_path='assets/enemies/enemy_1', center=(130, 279)):

        # attributes
        self.max_health = 0
        self.health = 1

        # movement
        self.speed = 5
        self.direction = pygame.math.Vector2(0, 0)
        self.path = [(-100, 349), (0, 349), (281, 358), (388, 427), (842, 440), (943, 402), (992, 287), (1033, 145),
                     (1151, 102), (1304, 149), (1335, 295), (1405, 395), (1537, 435), (1659, 513), (1669, 659),
                     (1585, 753), (1182, 783), (1057, 860), (259, 853), (142, 738), (109, 581), (0, 515), (-100, 515)]
        self.path_pos = 0
        self.x = self.path[self.path_pos][0]
        self.y = self.path[self.path_pos][1]
        self.center = center

        # animations
        self.folder_path = folder_path
        self.animations = import_animations(os.path.join(self.folder_path))
        self.status = 'run'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.animation_speed = .5
        self.facing_right = True

    def animate(self):

        current_animation = self.animations[self.status]

        # animation loop
        self.frame_index += self.animation_speed
        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        # get the current animation frame
        image = current_animation[math.floor(self.frame_index)]

        # flipping the image if needed
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False).convert_alpha()

        self.image = image

    def move(self):
        """Move enemy"""

        dirn = self.direction
        move_x, move_y = dirn[0] * self.speed, dirn[1] * self.speed

        self.x += move_x
        self.y += move_y

    def check_point_reached(self):
        """Check if the next point is reached"""

        dirn = self.direction
        x2, y2 = self.path[self.path_pos]

        # Go to next point
        if dirn[0] >= 0:  # moving right
            self.facing_right = True
            if dirn[1] >= 0:  # moving down
                if self.x >= x2 and self.y >= y2:
                    self.update_direction()
            else:  # moving up
                if self.x >= x2 and self.y <= y2:
                    self.update_direction()
        else:  # moving left
            self.facing_right = False
            if dirn[1] >= 0:  # moving down
                if self.x <= x2 and self.y >= y2:
                    self.update_direction()
            else:  # moving up
                if self.x <= x2 and self.y <= y2:
                    self.update_direction()

    def update_direction(self):
        """updates the next point to reach and changes the enemy direction accordingly"""

        self.path_pos += 1
        if self.path_pos >= len(self.path):
            self.path_pos = 0

        x1, y1 = self.x, self.y
        x2, y2 = self.path[self.path_pos]

        dirn = ((x2 - x1) * 2, (y2 - y1) * 2)
        length = math.sqrt((dirn[0]) ** 2 + (dirn[1]) ** 2)
        dirn = (dirn[0] / length, dirn[1] / length)

        self.direction = dirn

    def draw(self, surface):

        if self.facing_right:
            x_offset = self.center[0]
        else:
            x_offset = self.image.get_width() - self.center[0]
        y_offset = self.center[1]

        surface.blit(self.image, (self.x - x_offset, self.y - y_offset))

    def update(self):

        self.check_point_reached()
        self.move()
        self.animate()
