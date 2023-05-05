import pygame


class Button:

    def __init__(self, image: pygame.Surface, pos: tuple, on_click=None):

        self.on_click = on_click
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])

    def draw(self, screen):
        # draws the button

        screen.blit(self.image, self.rect)

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