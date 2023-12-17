import pygame


class Cursor(pygame.sprite.Sprite):
    def __init__(self, image, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = pygame.mouse.get_pos()
