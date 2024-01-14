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
        self.frames = ['#ff0000', '#cc0000', '#990000', '#660000', '#330000',
                       '#000000']
        self.frames = self.frames + self.frames[:-1][::-1]
        self.cur_frame = 0
        self.time_count = 0

    def render(self, count):
        font = pygame.font.Font(None, 100)
        if count:
            count_label = font.render(str(count), True, '#d5d6db')
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
            'coal': 0,
            'iron': 0,
            'gold': 0,
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
                                      True, '#d5d6db')
            self.screen.blit(output, (20, y))
            y += 60

    def update(self):
        if self.already_rendered < self.render_count:
            self.time_count += 1
            if self.time_count == 15:
                self.already_rendered += 1
                self.current_rendering[self.rendering[self.cur_index]] = \
                self.resources[self.rendering[self.cur_index]]
                self.cur_index += 1
                self.time_count = 0

    def restart(self):
        self.resources = {
            'coal': 0,
            'iron': 0,
            'gold': 0,
        }
        self.rendering = []
        self.current_rendering = {}
        self.cur_index = 0
        self.time_count = 0
        self.render_count = len(self.rendering)
        self.already_rendered = 0


class PopUpWindow(Text):
    def __init__(self, screen, screen_size, heading, data):
        super().__init__(screen, screen_size)
        self.heading = heading
        self.data = data
        self.show = False

    def render(self):
        if self.show:
            y = 80

            heading = self.font.render(self.heading, True, '#405273')
            image = load_image('window.png')

            bg = pygame.Surface(
                (self.width, self.height))  # the size of your rect
            bg.set_alpha(128)  # alpha level
            bg.fill((0, 0, 0))  # this fills the entire surface
            self.screen.blit(bg, (0, 0))

            self.screen.blit(image, (self.width // 2 - image.get_width() // 2,
                                     self.height // 2 - image.get_height() // 2))
            for key in self.data:
                if self.data[key] != 0:
                    name = self.font.render(key.capitalize(), True,'#405273')
                    value = self.font.render(str(self.data[key]), True,'#405273')

                    self.screen.blit(name, (
                    self.width // 2 - image.get_width() // 2 + 40,
                    self.height // 2 - image.get_height() // 2 + y))
                    self.screen.blit(value, (
                        self.width // 2 + image.get_width() // 2 - 40 - value.get_width(),
                        self.height // 2 - image.get_height() // 2 + y))
                    y += 60

            self.screen.blit(heading,
                             (self.width // 2 - heading.get_width() // 2,
                              self.height // 2 - image.get_height() // 2 + 20))


class Settings(Text):
    def __init__(self, screen, screen_size, heading, text):
        super().__init__(screen, screen_size)
        self.heading = heading
        self.text = text
        self.show = False

    def render(self):
        if self.show:
            y = 80

            heading = self.font.render(self.heading, True, '#405273')
            image = load_image('window.png')
            output = self.font.render(self.text, True, '#405273')

            bg = pygame.Surface(
                (self.width, self.height))  # the size of your rect
            bg.set_alpha(128)  # alpha level
            bg.fill((0, 0, 0))  # this fills the entire surface
            self.screen.blit(bg, (0, 0))

            self.screen.blit(image, (self.width // 2 - image.get_width() // 2,
                                     self.height // 2 - image.get_height() // 2))

            self.screen.blit(output,
                             (self.width // 2 - image.get_width() // 2 + 40,
                              self.height // 2 - image.get_height() // 2 + y))

            self.screen.blit(heading,
                             (self.width // 2 - heading.get_width() // 2,
                              self.height // 2 - image.get_height() // 2 + 20))


class StatusBar(Text):
    def __init__(self, screen, screen_size):
        super().__init__(screen, screen_size)
        self.font = pygame.font.Font(None, 75)
        self.text = ''
        self.time_count = 120
        self.default = 120

    def render(self):
        output = self.font.render(self.text, True, '#d5d6db')
        if self.time_count > 0:
            self.time_count -= 1
        if self.time_count > 0:
            self.screen.blit(output,
                             (self.width // 2 - output.get_width() // 2,
                             20))


class Timer(Ui):
    def __init__(self, seconds, screen, screen_size):
        super().__init__(screen, screen_size)
        self.font = pygame.font.Font(None, 200)
        self.seconds = seconds
        self.time_count = 60

    def render(self):
        output = self.font.render(str(self.seconds), True, '#d5d6db')
        if self.seconds > 0:
            if self.time_count > 0:
                self.time_count -= 1
            if self.time_count == 0:
                self.time_count = 60
                self.seconds -= 1

            self.screen.blit(output, (self.width // 2 - output.get_width() // 2, self.height - output.get_height() - 20))