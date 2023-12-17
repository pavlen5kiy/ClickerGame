import pygame


class Text:
    def __init__(self, screen, screen_size):
        self.screen = screen
        self.width = screen_size[0]
        self.height = screen_size[1]
        self.font = pygame.font.Font(None, 100)

    def dig_count(self, count):
        if count:
            count_label = self.font.render(str(count), True, 'white')
        else:
            count_label = self.font.render(str(count), True, 'red')
        self.screen.blit(count_label, (20, 20))

    def game_over(self, board):
        text = self.font.render("Game Over!", True, 'white')
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2,
                           board.top + board.cell_size * board.height + 50))
