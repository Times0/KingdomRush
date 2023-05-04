import pygame


class Button:

    def __init__(self, image: pygame.Surface, pos: tuple):

        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect(x=pos[0], y=pos[1])

    def draw(self, screen):

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
