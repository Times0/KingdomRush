from menu import MainMenu
from level import Level


class Game:

    def __init__(self):

        self.gamestate = 'menu'
        self.main_menu = MainMenu(self.show_level)
        self.level = Level(self.show_menu)

    def show_level(self):
        self.gamestate = 'level'

    def show_menu(self):
        self.gamestate = 'menu'

    def run(self, events):
        if self.gamestate == 'menu':
            self.main_menu.run(events)
        elif self.gamestate == 'level':
            self.level.run(events)
