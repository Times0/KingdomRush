import pygame
from menu import MainMenu
import os
from level import Level
from constants import *


class Game:

    def __init__(self):

        self.gamestate = 'menu'
        self.main_menu = MainMenu(self.show_level)
        self.level = Level(self.show_menu)

    def show_level(self):
        pygame.mixer.music.play(loops=-1)
        self.gamestate = 'level'

    def show_menu(self):
        pygame.mixer.music.stop()
        self.gamestate = 'menu'

    def run(self, events, dt):
        if self.gamestate == 'menu':
            self.main_menu.run(events)
        elif self.gamestate == 'level':
            self.level.run(events, dt)
