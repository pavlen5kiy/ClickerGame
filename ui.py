import pygame
from image_controller import load_image


class Ui:
    def __init__(self, screen, screen_size):
        '''

        :type screen_size: tuple
        '''

        self.screen = screen
        self.width = screen_size[0]
        self.height = screen_size[1]


class Text(Ui):
    def __init__(self, screen, screen_size):
        super().__init__(screen, screen_size)
        self.font = pygame.font.Font(None, 75)


class DigCount(Text):
    def __init__(self, screen, screen_size):
        super().__init__(screen, screen_size)
        self.font = pygame.font.Font(None, 100)

    def render(self, count):
        font = pygame.font.Font(None, 100)
        if count:
            count_label = font.render(str(count), True, 'white')
        else:
            count_label = font.render(str(count), True, 'red')
        self.screen.blit(count_label, (20, 20))


class Table(Text):
    def __init__(self, screen, screen_size):
        super().__init__(screen, screen_size)
        self.resources = {
            'Coal': 0,
            'Iron': 0,
            'Gold': 0,
            'Artifact': 0,
            'Diamond': 0
        }

    def render(self):
        y = 100
        for key in self.resources:
            if self.resources[key] != 0:
                output = self.font.render(f'{key}: {self.resources[key]}',
                                          True, 'white')
                self.screen.blit(output, (20, y))
                y += 60
