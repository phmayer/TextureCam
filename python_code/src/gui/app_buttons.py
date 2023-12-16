import pygame

class Button:
    def __init__(self,screen, x, y, image_up, image_down, action=None):
        self.image_up = image_up
        self.image_down = image_down
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.action = action
        self.clicked = False
        self.current_screen = screen
    def draw(self):
        self.current_screen.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                self.image = self.image_down
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.clicked:
                self.clicked = False
                self.image = self.image_up
                if self.rect.collidepoint(event.pos) and self.action:
                    self.action()
