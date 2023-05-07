import pygame
from buttons import Item
import os
from constants import *
from data import items_data


class VerticalShop:

    def __init__(self, side, item_names):

        # Import background image :
        bg_path = 'assets/shop/side.png'
        self.background = pygame.image.load(os.path.join(bg_path)).convert_alpha()

        self.height = 20
        self.width = 150

        # Create all the items and position them correctly
        btn_x = 0
        btn_y = 15
        y_margin = 20  # pixels between each item
        self.items = []
        for name in item_names:
            item = self.create_item(name, btn_x, btn_y)
            btn_y += item.height + y_margin
            self.items.append(item)
        self.height += btn_y - y_margin

        # resize background based on the items that are in it
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # position the whole menu
        screen_border_margin = 15
        if side == 'right':
            self.x = WINDOW_WIDTH - self.background.get_width() - screen_border_margin
        elif side == 'left':
            self.x = screen_border_margin
        else:
            raise Exception('"side" parameter must be either "left" or "right"')
        self.y = (WINDOW_HEIGHT - self.background.get_height()) / 2

    def create_item(self, name, btn_x, btn_y):

        data = items_data[name]
        image = pygame.image.load(os.path.join(items_data['path'], data[0])).convert_alpha()
        image = pygame.transform.scale_by(image, .5)
        cost = data[1]
        item = Item(image, (btn_x, btn_y), self.width, name, cost)
        return item

    def draw(self, surface):
        surface.blit(self.background, (self.x, self.y))

        for item in self.items:
            item.draw(self.background)
