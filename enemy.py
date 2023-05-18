import math

import pygame

from assets import ogre_animations, pekka_animations, armored_ogre_animations, scorpion_animations, wizard_animations

ENEMY_PATH = [(2000, 139), (1898, 139), (782, 131), (668, 259), (682, 405), (787, 485), (1059, 481), (1208, 534),
              (1237, 681),
              (1152, 807), (849, 823), (670, 823), (578, 771), (515, 772), (451, 816), (327, 784), (227, 740),
              (0, 734), (-50, 734)]


class Enemy:
    def __init__(self, animations=None, center=(130, 279), health=3, money=100):

        # attributes
        self.max_health = health
        self.health = self.max_health
        self.money = money
        self.dead = False
        self.off_screen = False

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
            self.off_screen = True
        else:
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

    def draw_health_bar(self, surface):
        """
        draw health bar above enemy
        """

        full_length = 50
        health_percent = self.health / self.max_health
        health_length = round(health_percent * full_length)

        pygame.draw.rect(surface, (255, 0, 0), (self.x - 30, self.y - 120, full_length, 10), 0)
        pygame.draw.rect(surface, (0, 255, 0), (self.x - 30, self.y - 120, health_length, 10), 0)

    def draw(self, surface):

        if self.facing_right:
            x_offset = self.center[0]
        else:
            x_offset = self.image.get_width() - self.center[0]
        y_offset = self.center[1]

        surface.blit(self.image, (self.x - x_offset, self.y - y_offset))
        self.draw_health_bar(surface)

    def update(self, dt):
        if self.status != 'die':
            self.check_point_reached()
            self.move(dt)
        self.animate(dt)


class Scorpion(Enemy):

    def __init__(self):
        self.animations = scorpion_animations
        super().__init__(animations=self.animations, center=(50, 75))

        self.max_health = 3
        self.health = self.max_health
        self.money = 50
        self.speed = 250


class Wizard(Enemy):

    def __init__(self):
        self.animations = wizard_animations
        super().__init__(animations=self.animations, center=(40, 70))

        self.max_health = 10
        self.health = self.max_health
        self.money = 100
        self.speed = 150


class Ogre(Enemy):

    def __init__(self):
        self.animations = ogre_animations
        super().__init__(animations=self.animations, center=(65, 140))

        self.max_health = 20
        self.health = self.max_health
        self.money = 150
        self.speed = 175


class ArmoredOgre(Enemy):

    def __init__(self):
        self.animations = armored_ogre_animations
        super().__init__(animations=self.animations, center=(45, 120))

        self.max_health = 50
        self.health = self.max_health
        self.money = 200
        self.speed = 175


class Pekka(Enemy):

    def __init__(self):
        self.animations = pekka_animations
        super().__init__(animations=self.animations, center=(70, 125))

        self.max_health = 100
        self.health = self.max_health
        self.money = 500
        self.speed = 200
