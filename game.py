import pygame
from menu import MainMenu
from level import Level


class Game:

    def __init__(self):

        self.game_state = 'menu'
        self.main_menu = MainMenu(self.create_level)
        self.level = Level(self.show_menu)

    def create_level(self):
        self.level = None
        self.level = Level(self.show_menu)
        self.show_level()

    def show_level(self):
        pygame.mixer.music.play(loops=-1)
        self.game_state = 'level'

    def show_menu(self):
        pygame.mixer.music.stop()
        self.game_state = 'menu'

    def run(self, events, dt):
        if self.game_state == 'menu':
            self.main_menu.run(events)
        elif self.game_state == 'level':
            self.level.run(events, dt)
