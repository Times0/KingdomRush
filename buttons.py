import pygame


class Button:

    def __init__(self, image: pygame.Surface, pos: tuple, on_click=None):

        self.on_click = on_click
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])

    def draw(self, surface):
        # draws the button

        surface.blit(self.image, self.rect)

    def on_mouse_clicked(self, event):
        # returns true if button clicked

        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)

    def on_mouse_motion(self, event):
        # returns true if hovered

        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                return True
            else:
                return False


class ToggleButton(Button):

    def __init__(self, images: list, pos: tuple, on_click=None):

        first_image = images[0]
        super().__init__(first_image, pos, on_click)

        self.images = images
        self.image_index = 0
        self.image = images[self.image_index]

    def on_mouse_clicked(self, event):
        # returns true if button clicked

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
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


class Item:

    def __init__(self, image, pos, menu_width, name, cost, on_click=None):
        self.width = menu_width
        self.name = name
        self.cost = cost
        self.image = image
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        btn_x = (self.width - self.image.get_width()) / 2
        self.button = Button(image, (btn_x, pos[1]), on_click)

        self.font = pygame.font.SysFont("comicsans", 20)
        self.text_image = self.font.render(str(self.cost), False, (255, 255, 255)).convert_alpha()

        self.star_image = pygame.image.load("assets/shop/star.png").convert_alpha()
        self.star_image = pygame.transform.scale_by(self.star_image,
                                                    (self.text_image.get_height() / self.star_image.get_height()))

        text_x = self.width / 2 - (self.text_image.get_width()) / 2
        self.text_pos = (self.x + text_x, self.y + self.image.get_width())
        star_x = text_x - self.star_image.get_width() - 5
        self.star_pos = (self.x + star_x, self.y + self.image.get_height())

        self.height = self.image.get_height() + self.text_image.get_height()

        self.surface = pygame.Surface((self.width, self.height)).convert_alpha()
        self.surface.set_colorkey((0, 0, 0))
        self.surface.blit(self.image, (0, 0))
        self.surface.blit(self.star_image, (0, self.image.get_height()))
        self.surface.blit(self.text_image, (self.star_image.get_width(), self.image.get_height()))

        self.rect = self.surface.get_rect()

    def draw(self, surface):
        self.button.draw(surface)
        surface.blit(self.star_image, self.star_pos)
        surface.blit(self.text_image, self.text_pos)
