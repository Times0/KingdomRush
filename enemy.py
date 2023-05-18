import math

import pygame

from assets import ogre_animations

ENEMY_PATH = [(2000, 139), (1898, 139), (782, 131), (668, 259), (682, 405), (787, 485), (1059, 481), (1208, 534),
              (1237, 681),
              (1152, 807), (849, 823), (670, 823), (578, 771), (515, 772), (451, 816), (327, 784), (227, 740),
              (0, 734)]


class Enemy:
    def __init__(self, animations=None, center=(130, 279), health=3, money=100):

        # attributes
        self.health = health
        self.money = money
        self.dead = False

        # movement
        self.center = center
        self.speed = 100
        self.direction = pygame.math.Vector2(0, 0)
        self.path = ENEMY_PATH
        self.path_pos = 0
        self.x = self.path[self.path_pos][0]
        self.y = self.path[self.path_pos][1]

        # animations
        self.animations = animations
        self.status = 'run'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.animation_speed = 30
        self.facing_right = True

    def animate(self, dt):

        current_animation = self.animations[self.status]

        # animation loop
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(current_animation):
            # go back to the first frame of the animation
            if self.status == 'die':
                self.dead = True
            self.frame_index = 0

        # get the current animation frame
        image = current_animation[math.floor(self.frame_index)]

        # flipping the image if needed
        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        self.image = image

    def move(self, dt):
        """Move enemy"""

        dirn = self.direction
        move_x, move_y = dirn[0] * self.speed * dt, dirn[1] * self.speed * dt

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

    def hit(self, damage):

        self.health -= damage
        if self.health <= 0:
            self.status = 'die'
            self.frame_index = 0

    def check_death(self):

        if self.health <= 0:
            self.status = 'die'
            return True
        else:
            return False

    def draw(self, surface):

        if self.facing_right:
            x_offset = self.center[0]
        else:
            x_offset = self.image.get_width() - self.center[0]
        y_offset = self.center[1]

        surface.blit(self.image, (self.x - x_offset, self.y - y_offset))

    def update(self, dt):
        if self.status != 'die':
            self.check_point_reached()
            self.move(dt)
        self.animate(dt)


class Ogre(Enemy):

    def __init__(self):
        self.health = 100
        self.money = 100
        self.animations = ogre_animations

        super().__init__(animations=self.animations, center=(130, 279), health=self.health, money=self.money)
