import pygame
from buttons import Item
import os
from constants import *
from data import items_data


class VerticalShop:

    def __init__(self, items, width=150, y_margin=0):

        self.items = items

        self.x = 0
        self.y = 0

        # Import background image :
        bg_path = 'assets/shop/side.png'
        self.background = pygame.image.load(os.path.join(bg_path)).convert_alpha()
        self.background.set_alpha(255)

        self.width = width
        self.y_margin = y_margin
        self.height = (self.items[0].height + self.y_margin) * len(self.items) + 20

        # resize background based on the items that are in it
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

    def draw(self, surface):

        surface.blit(self.background, (self.x, self.y))

        for item in self.items:
            item.draw(surface, (self.x, self.y))

    def update(self, event_pos):

        shop_pos = (event_pos[0] - self.x, event_pos[1] - self.y)

        for item in self.items:
            button = item.button

            if button.on_mouse_clicked(shop_pos):
                # button clicked
                if button.on_click:
                    button.on_click()


class MainShop(VerticalShop):

    def __init__(self, side, item_names, buy_item):

        self.buy_item = buy_item

        self.width = 150
        self.height = 0

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

        super().__init__(self.items, width=self.width, y_margin=y_margin)

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
        on_click = self.buy_item
        item = Item(image, (btn_x, btn_y), self.width, name, cost, on_click=on_click)
        return item

    def update(self, event_pos):

        shop_pos = (event_pos[0] - self.x, event_pos[1] - self.y)

        for item in self.items:
            button = item.button

            if button.on_mouse_clicked(shop_pos):
                # button clicked
                if button.on_click:
                    button.on_click(event_pos, item.name)
