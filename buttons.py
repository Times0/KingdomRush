import pygame


class Button:

    def __init__(self, image: pygame.Surface, pos: tuple, on_click=None):

        self.on_click = on_click
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])

    def draw(self, surface, pos=(0, 0)):
        # draws the button
        x = pos[0] + self.rect.x
        y = pos[1] + self.rect.y
        surface.blit(self.image, (x, y))

    def on_mouse_clicked(self, event_pos):
        # returns true if button clicked

        return self.rect.collidepoint(event_pos)

    def on_mouse_motion(self, event_pos):
        # returns true if hovered

        if self.rect.collidepoint(event_pos):
            return True
        else:
            return False


class ToggleButton(Button):

    def __init__(self, images: list, pos: tuple, on_click_actions=None):

        if on_click_actions is None:
            self.on_click_actions = []
            self.on_click = None
        else:
            self.on_click_actions = on_click_actions
            self.on_click = on_click_actions[0]

        first_image = images[0]

        super().__init__(first_image, pos, on_click=self.on_click)

        self.images = images
        self.image_index = 0
        self.image = images[self.image_index]
        if len(self.on_click_actions) > 0:
            self.on_click = self.on_click_actions[self.image_index]

    def on_mouse_clicked(self, event_pos):
        # returns true if button clicked

        if len(self.on_click_actions) > 0:
            self.on_click = self.on_click_actions[self.image_index]
        if self.rect.collidepoint(event_pos):
            self.change_image()
            return True

        else:
            return False

    def change_image(self):
        # changes button image on click

        self.image_index += 1
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.image = self.images[self.image_index]

    def toggle(self):

        self.change_image()
        if len(self.on_click_actions) > 0:
            self.on_click = self.on_click_actions[self.image_index]


class Item:

    def __init__(self, image, pos, menu_width, name, cost, assets_path=None, on_click=None):
        # position relative to menu
        self.width = menu_width
        self.name = name
        self.cost = cost
        self.image = image
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.assets_path = assets_path
        btn_x = (self.width - self.image.get_width()) / 2
        self.button = Button(image, (btn_x, pos[1]), on_click)

        self.font = pygame.font.SysFont("arial", 20)
        self.text_image = self.font.render(str(self.cost), 1, (255, 255, 255)).convert_alpha()

        self.star_image = pygame.image.load("assets/shop/star.png").convert_alpha()
        self.star_image = pygame.transform.scale_by(self.star_image,
                                                    (self.text_image.get_height() / self.star_image.get_height()))

        self.star_pos = (self.x + btn_x, self.y + self.image.get_height())
        self.text_pos = (self.star_pos[0] + self.star_image.get_width() + 5, self.y + self.image.get_height())

        self.height = self.image.get_height() + self.text_image.get_height()

        # self.surface = pygame.Surface((self.width, self.height)).convert_alpha()
        # self.surface.set_colorkey((0, 0, 0))
        # self.surface.blit(self.image, (0, 0))
        # self.surface.blit(self.star_image, (0, self.image.get_height()))
        # self.surface.blit(self.text_image, (self.star_image.get_width(), self.image.get_height()))
        #
        # self.rect = self.surface.get_rect()

    def change_cost(self, new_cost):
        self.cost = new_cost
        self.text_image = self.font.render(str(new_cost), 1, (255, 255, 255)).convert_alpha()
        self.text_pos = (self.star_pos[0] + self.star_image.get_width() + 5, self.y + self.image.get_height())

    def draw(self, surface, pos):
        self.button.draw(surface, pos)
        surface.blit(self.star_image, (pos[0] + self.star_pos[0], pos[1] + self.star_pos[1]))
        surface.blit(self.text_image, (pos[0] + self.text_pos[0], pos[1] + self.text_pos[1]))
