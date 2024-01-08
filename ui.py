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
        self.color = '#ff0000'
        self.frames = ['#ff0000', '#cc0000', '#990000', '#660000', '#330000', '#000000']
        self.frames = self.frames + self.frames[:-1][::-1]
        self.cur_frame = 0
        self.time_count = 0

    def render(self, count):
        font = pygame.font.Font(None, 100)
        if count:
            count_label = font.render(str(count), True, 'white')
        else:
            count_label = font.render(str(count), True, self.color)
        self.screen.blit(count_label, (20, 20))

    def update(self):
        self.time_count += 1
        if self.time_count == 5:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.color = self.frames[self.cur_frame]
            self.time_count = 0


class Table(Text):
    def __init__(self, screen, screen_size):
        super().__init__(screen, screen_size)
        self.resources = {
            'Coal': 0,
            'Iron': 0,
            'Gold': 0,
        }
        self.rendering = []
        self.current_rendering = {}
        self.cur_index = 0
        self.time_count = 0
        self.render_count = len(self.rendering)
        self.already_rendered = 0

    def render(self):
        y = 100
        for key in self.current_rendering:
            output = self.font.render(f'{key}: {self.current_rendering[key]}',
                                      True, 'white')
            self.screen.blit(output, (20, y))
            y += 60

    def update(self):
        if self.already_rendered < self.render_count:
            self.time_count += 1
            if self.time_count == 10:
                self.already_rendered += 1
                self.current_rendering[self.rendering[self.cur_index]] = self.resources[self.rendering[self.cur_index]]
                self.cur_index += 1
                self.time_count = 0

    def restart(self):
        self.resources = {
            'Coal': 0,
            'Iron': 0,
            'Gold': 0,
        }
        self.rendering = []
        self.current_rendering = {}
        self.cur_index = 0
        self.time_count = 0
        self.render_count = len(self.rendering)
        self.already_rendered = 0
