import pygame


class Table:
    def __init__(self):
        self.resources = {
            'Coal': 0,
            'Iron': 0,
            'Gold': 0,
            'Artifact': 0,
            'Diamond': 0
        }

    def render(self, screen):
        font = pygame.font.Font(None, 100)
        y = 100
        for key in self.resources:
            if self.resources[key] != 0:
                output = font.render(f'{key}: {self.resources[key]}', True, 'white')
                screen.blit(output, (20, y))
                y += 70
