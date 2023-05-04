import sys

import pygame
from constants import *
import os
from ui import Button


class MainMenu:
    def __init__(self):
        self.screen = pygame.display.get_surface()

        # Import background image
        bg_path = '../game_assets/bg.png'
        self.background = pygame.image.load(os.path.join(bg_path))
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Button 1 :
        # Import button image:
        btn_path = '../game_assets/button_start.png'
        self.btn_image = pygame.image.load(os.path.join(btn_path)).convert_alpha()

        # Position button:
        btn_width = self.btn_image.get_width()
        btn_height = self.btn_image.get_height()
        btn_x = (WINDOW_WIDTH - btn_width) / 2
        btn_y = (WINDOW_HEIGHT - btn_height) / 2

        self.btn = Button(self.btn_image, (btn_x, btn_y))

    def run(self, events):

        # event handler
        for event in events:

            # quitting game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn.on_mouse_clicked(event):
                    # button clicked
                    print('button clicked')

            elif event.type == pygame.MOUSEMOTION:
                if self.btn.on_mouse_motion(event):
                    # button hovered
                    pass

        # Background
        self.screen.blit(self.background, (0, 0))

        # Button
        self.btn.draw(self.screen)

        # Updating screen
        pygame.display.flip()
