import pygame
from menu import Menu
from level import Level

class Game :

    def __init__(self):

        self.gamestate = 'menu'
        self.menu = Menu()
        self.level = Level()

    def run(self, events):
        if self.gamestate == 'menu':
            self.menu.run(events)
        elif self.gamestate == 'level':
            self.level.run(events)