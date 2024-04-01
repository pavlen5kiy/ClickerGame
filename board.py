import random
import pygame
from image_controller import load_image, rescale_image
from constants import RESOURCES_INDEXES
from ui import Table
from sprite_controller import create_particles, generate_particles
from sound_controller import play_sound


class Board:

    # Creating board
    def __init__(self, score, width, height):

        '''

        :type width: int
        :type height: int
        :type count: int
        '''
        self.score = score
        self.width = width
        self.height = height
        self.board = [[0] * self.width for _ in range(self.height)]
        # Defaults
        self.left = 10
        self.top = 10
        self.cell_size = 120
        self.clicked = []
        self.count = 5
        self.max_count = 5
        self.layers = 1

        self.states = [load_image('stone.png'),
                       load_image('coal.png'),
                       load_image('iron.png'),
                       load_image('gold.png'),
                       [load_image('sigma.png'),
                        rescale_image(load_image('ipuchi.jpg')),
                        rescale_image(load_image('skull.jpeg'))],
                       load_image('diamond.png')]

    def render(self, screen):

        '''
        Draws a board
        '''

        # Borders
        pygame.draw.rect(screen, pygame.Color('#a57855'), (
            self.left - 3, self.top - 3, self.width * self.cell_size + 6,
            self.height * self.cell_size + 6), 3)

        # Cells
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

    def set_view(self, left, top, cell_size):

        '''
        Sets board's position and cell size
        :type left: int
        :type top: int
        :type cell_size: int
        '''

        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):

        '''
        Gets list indexes of pressed cell
        :type mouse_pos: tuple
        :return: cell's coordinates in list
        '''

        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or \
                cell_y < 0 or cell_x >= self.height:
            return
        return cell_x, cell_y

    def on_click(self, cell, table, particles_group):

        '''
        Randomly generates resources after cell was clicked
        :type cell: tuple
        :type table: Table
        '''

        create_particles(pygame.mouse.get_pos(),
                         generate_particles('sand_particle.png'),
                         20,
                         particles_group)

        state = random.choices(self.states,
                               weights=(35, 35, 15, 8, 5, 2), k=1)[0]
        index = self.states.index(state)

        if index:
            if index == 5:
                amount = \
                random.choices(range(1, 6), weights=(50, 20, 15, 10, 5), k=1)[
                    0]
                self.score['gems'] += amount

                create_particles(pygame.mouse.get_pos(),
                                 generate_particles('gem.png'),
                                 amount,
                                 particles_group)

            elif index == 4:
                state = random.choice(self.states[4])
                amount = \
                random.choices(range(20, 50), weights=tuple(range(90, 0, -3)),
                               k=1)[0]
                self.score['coins'] += amount

                create_particles(pygame.mouse.get_pos(),
                                 generate_particles('coin.png'),
                                 amount // 2,
                                 particles_group)
            else:
                resource = RESOURCES_INDEXES[index]
                self.score[resource] += 1
                table.resources[resource] += 1

        self.board[cell[1]][cell[0]] = state
        self.clicked.append(cell)

    def get_click(self, mouse_pos, table, particles_group):

        '''
        Activates resources generation and decreases dig count
        :type mouse_pos: tuple
        :type table: Table
        '''

        cell = self.get_cell(mouse_pos)
        if cell and cell not in self.clicked:
            self.on_click(cell, table, particles_group)
            self.count -= 1

    def restart(self):
        self.board = [[0] * self.width for _ in range(self.height)]
        self.count = self.max_count
        self.clicked = []
