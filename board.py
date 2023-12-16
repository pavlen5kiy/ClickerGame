import pygame
from image_loader import load_image

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.clicked = []

    def render(self, screen):
        cell_image = load_image('tile.png')
        cell_image = pygame.transform.scale(cell_image,
                                            (self.cell_size, self.cell_size))
        pygame.draw.rect(screen, pygame.Color('#977d54'), (
        self.left - 3, self.top - 3, self.width * self.cell_size + 6,
        self.height * self.cell_size + 6), 3)

        for y in range(self.height):
            for x in range(self.width):
                # pygame.draw.rect(screen, colors[self.board[y][x]], (
                #     x * self.cell_size + self.left,
                #     y * self.cell_size + self.top,
                #     self.cell_size, self.cell_size))
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, pygame.Color('black'), (
                        x * self.cell_size + self.left,
                        y * self.cell_size + self.top,
                        self.cell_size, self.cell_size))
                else:
                    screen.blit(cell_image, (
                        x * self.cell_size + self.left,
                        y * self.cell_size + self.top,
                        self.cell_size, self.cell_size))

                # pygame.draw.rect(screen, pygame.Color('gray'), (
                #     x * self.cell_size + self.left,
                #     y * self.cell_size + self.top,
                #     self.cell_size, self.cell_size), 2)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or \
                cell_y < 0 or cell_x >= self.height:
            return
        return cell_x, cell_y

    def on_click(self, cell):
        if cell not in self.clicked:
            self.board[cell[1]][cell[0]] = (self.board[cell[1]][
                                                cell[0]] + 1) % 2
            self.clicked.append(cell)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
