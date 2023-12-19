import pygame


class Ui:
    def __init__(self, screen, screen_size):
        '''

        :type screen_size: tuple
        '''

        self.screen = screen
        self.width = screen_size[0]
        self.height = screen_size[1]
        self.font = pygame.font.Font(None, 75)


class Text(Ui):
    def __init__(self, screen, screen_size):
        super().__init__(screen, screen_size)

    def dig_count(self, count):
        font = pygame.font.Font(None, 100)
        if count:
            count_label = font.render(str(count), True, 'white')
        else:
            count_label = font.render(str(count), True, 'red')
        self.screen.blit(count_label, (20, 20))

    def game_over(self, board):
        text = self.font.render("Game Over!", True, 'white')
        self.screen.blit(text, (20,
                                board.top + board.cell_size * board.height -
                                text.get_height()))


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

    def render(self, screen):
        y = 100
        for key in self.resources:
            if self.resources[key] != 0:
                output = self.font.render(f'{key}: {self.resources[key]}',
                                          True, 'white')
                screen.blit(output, (20, y))
                y += 60
