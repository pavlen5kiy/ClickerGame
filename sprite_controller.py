import pygame
from image_controller import load_image
from constants import GRAVITY
import random


class Sprite(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)


class Cursor(Sprite):
    def __init__(self, image, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()

    def update(self, render=False):
        if render:
            self.rect.topleft = pygame.mouse.get_pos()
        else:
            self.rect.topleft = (9999, 9999)


class Button(Sprite):
    def __init__(self, image, highlight, pos=(0, 0), *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.orig = image
        self.highlight = highlight
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, *args):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.x <= mouse_pos[
            0] <= self.rect.x + self.orig.get_width() and self.rect.y <= \
                mouse_pos[1] <= self.rect.y + self.orig.get_height():
            self.image = self.highlight
        else:
            self.image = self.orig

        if (args and args[0].type == pygame.MOUSEBUTTONDOWN and
                self.rect.collidepoint(args[0].pos)):
            return True


class Particle(Sprite):
    def __init__(self, pos, dx, dy, particles, *group):
        super().__init__(*group)
        self.particles = particles
        self.image = random.choice(self.particles)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITY

    def update(self, screen_rect):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()
