import random
import pygame
from image_loader import load_image, rescale_image
from constants import RESOURCES_INDEXES


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

        self.count = 20

        self.states = [rescale_image(load_image('stone.png')),
                       rescale_image(load_image('coal.png')),
                       rescale_image(load_image('iron.png')),
                       rescale_image(load_image('gold.png')),
                       rescale_image(load_image('artifact.png')),
                       rescale_image(load_image('diamond.png'))]


    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color('#977d54'), (
        self.left - 3, self.top - 3, self.width * self.cell_size + 6,
        self.height * self.cell_size + 6), 3)

        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != 0:
                    screen.blit(self.board[y][x], (
                        x * self.cell_size + self.left,
                        y * self.cell_size + self.top,
                        self.cell_size, self.cell_size))
                else:
                    screen.blit(load_image('tile.png'), (
                        x * self.cell_size + self.left,
                        y * self.cell_size + self.top,
                        self.cell_size, self.cell_size))

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

    def on_click(self, cell, table):
        state = random.choices(self.states, weights=(40, 25, 20, 8, 5, 2), k=1)[0]
        index = self.states.index(state)
        if index:
            resource = RESOURCES_INDEXES[index]
            table.resources[resource] += 1
        self.board[cell[1]][cell[0]] = state
        self.clicked.append(cell)

    def get_click(self, mouse_pos, table):
        cell = self.get_cell(mouse_pos)
        if cell and cell not in self.clicked:
            self.on_click(cell, table)
            self.count -= 1
