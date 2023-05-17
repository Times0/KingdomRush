import os
import sys

import pygame

from buttons import Button, ToggleButton
from constants import *


class MainMenu:
    def __init__(self, show_level):
        self.screen = pygame.display.get_surface()
        self.show_level = show_level

        # Import background image
        bg_path = 'assets/main_menu/bg.png'
        self.background = pygame.image.load(os.path.join(bg_path))
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Buttons list :
        self.buttons = list()

        # Start button :
        btn_path = 'assets/main_menu/button_play.png'
        btn_image = pygame.image.load(os.path.join(btn_path)).convert_alpha()
        btn_width = btn_image.get_width()
        btn_height = btn_image.get_height()
        btn_x = (WINDOW_WIDTH - btn_width) / 2
        btn_y = (WINDOW_HEIGHT - btn_height) / 2

        self.start_btn = Button(btn_image, (btn_x, btn_y), on_click=self.show_level)
        self.buttons.append(self.start_btn)

        # Settings button :
        btn_path = 'assets/main_menu/button_close.png'
        btn_image = pygame.image.load(os.path.join(btn_path)).convert_alpha()
        btn_width = btn_image.get_width()
        offset = 10
        btn_x = WINDOW_WIDTH - btn_width - offset
        btn_y = offset

        self.close_btn = Button(btn_image, (btn_x, btn_y), on_click=exit)
        self.buttons.append(self.close_btn)

        # Sound button :
        sound_on_path = 'assets/main_menu/button_sound.png'
        sound_on_image = pygame.image.load(os.path.join(sound_on_path)).convert_alpha()
        sound_off_path = 'assets/main_menu/button_sound_off.png'
        sound_off_image = pygame.image.load(os.path.join(sound_off_path)).convert_alpha()
        offset = 10
        btn_x = offset
        btn_y = offset

        self.close_btn = ToggleButton([sound_on_image, sound_off_image], (btn_x, btn_y))
        self.buttons.append(self.close_btn)

    def run(self, events):
        # event handler
        for event in events:
            # quitting game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.on_mouse_clicked(event.pos):
                        # button clicked
                        if button.on_click:
                            button.on_click()

            elif event.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    if button.on_mouse_motion(event.pos):
                        # button hovered
                        pass

        # Background
        self.screen.blit(self.background, (0, 0))

        # Button
        for button in self.buttons:
            button.draw(self.screen)

        # Updating screen
        pygame.display.flip()
