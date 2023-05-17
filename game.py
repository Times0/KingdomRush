from level import Level
from menu import MainMenu


class Game:

    def __init__(self):

        self.game_state = 'menu'
        self.main_menu = MainMenu(self.show_level)
        self.level = Level(self.show_menu)

    def show_level(self):
        self.game_state = 'level'

    def show_menu(self):
        self.game_state = 'menu'

    def run(self, events, dt):
        if self.game_state == 'menu':
            self.main_menu.run(events)
        elif self.game_state == 'level':
            self.level.run(events, dt)
