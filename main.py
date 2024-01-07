import random
import sys
import math

import pygame
from board import Board
from image_controller import load_image
from ui import Table, DigCount
from money import Money
from sprite_controller import Cursor, Button


def terminate():
    pygame.quit()
    sys.exit()


def log(output):
    print(f'LOG: ', output)


def screen_init():
    # Setting a game window with computer's screen size
    screen_info = pygame.display.Info()
    screen_size = screen_info.current_w, screen_info.current_h
    log(f'screen resolution {screen_size}')
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    sreen_rect = (0, 0, screen_size[0], screen_size[1])

    pygame.display.set_caption('Board dev')

    return screen, screen_size, sreen_rect


def background(screen_size, tiles=None, rand=False, weights=None):
    width, height = screen_size
    im_width, im_height = 120, 120

    # Calculate how many tiles we need to draw in x-axis and y-axis
    x_tiles = math.ceil(width / im_width)
    y_tiles = math.ceil(height / im_height)

    if rand:
        bg = [[random.choices(tiles, weights=weights, k=1)[0] for x in
               range(x_tiles)] for y in range(y_tiles - 1)]
        bg.append([load_image('cliff.png')] * x_tiles)

        return bg, x_tiles, y_tiles
    return x_tiles, y_tiles


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen, screen_size, screen_rect = screen_init()

    mode = 1

    # MENU

    # Sprites
    super_group = pygame.sprite.Group()
    cursor_image = load_image("cursor.png")
    cursor = Cursor(cursor_image, super_group)

    main_menu = pygame.sprite.Group()
    db_image = load_image("map.png")
    dig_button = Button(db_image, load_image('map_highlited.png'),
                        (
                            300,
                            screen_size[1] // 2 - db_image.get_height() // 2),
                        main_menu)

    wh_image = load_image("workshop.png")
    workshop_button = Button(wh_image,
                             load_image('workshop_highlited.png'),
                             (
                                 screen_size[0] - wh_image.get_width() - 300,
                                 screen_size[
                                     1] // 2 - wh_image.get_height() // 2),
                             main_menu)

    close_image = load_image("close.png")
    close_button = Button(close_image,
                          load_image('close_highlited.png'),
                          (10, screen_size[1] - close_image.get_height() - 10),
                          main_menu)

    # DIGGING
    width, height = screen_size

    calculated = False

    # Ui
    table = Table(screen, screen_size)
    money = Money(screen, screen_size)
    dig_count = DigCount(screen, screen_size)

    # Board
    size = 7, 7
    board = Board(money, *size)
    cell_size = 120
    left = width // 2 - board.width * cell_size // 2
    top = height // 2 - board.height * cell_size // 2
    board.set_view(left, top, cell_size)

    # Sprites
    dig_menu = pygame.sprite.Group()
    pickaxe_cursor = Cursor(load_image("pickaxe_cursor.png"), dig_menu)

    home_image = load_image("home.png")
    home_button_2 = Button(home_image,
                           load_image('home_highlited.png'),
                           (10, screen_size[1] - home_image.get_height() - 10), dig_menu)

    particles_group = pygame.sprite.Group()

    # WORKSHOP
    workshop_menu = pygame.sprite.Group()
    home_button_3 = Button(home_image,
                         load_image('home_highlited.png'),
                         (10, screen_size[1] - home_image.get_height() - 10), workshop_menu)

    storage_image = load_image("chest.png")
    storage_button = Button(storage_image,
                            load_image('chest_highlited.png'),
                            (screen_size[0] - storage_image.get_width() - 10,
                             screen_size[1] - home_image.get_height() - 10),
                            workshop_menu)

    powerup_image = load_image("powerup.png")
    powerup_button = Button(powerup_image,
                            load_image('powerup_highlited.png'),
                            (screen_size[0] - powerup_image.get_width() - storage_image.get_width() - 20,
                             screen_size[1] - home_image.get_height() - 10),
                            workshop_menu)

    running = True
    bg_drawn = False

    fps = 60

    while running:
        clock.tick(fps)

        if mode == 1:
            if not bg_drawn:
                # Loading background
                x_tiles, y_tiles = background(screen_size, rand=False)
                bg = load_image('wood.png')

                bg_drawn = True

            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(False)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if close_button.update(event):
                    running = False

                if dig_button.update(event):
                    mode = 2
                    bg_drawn = False

                if workshop_button.update(event):
                    mode = 3
                    bg_drawn = False

            # Drawing background
            for x in range(x_tiles):
                for y in range(y_tiles):
                    screen.blit(bg, (x * 120, y * 120))

            money.render()

            main_menu.draw(screen)

            # Cursor render
            super_group.draw(screen)
            cursor.update(True)

            pygame.display.flip()

        if mode == 2:
            if not bg_drawn:
                # Loading background
                tiles = [load_image('sand.png'),
                         load_image('sand_stone.png'),
                         load_image('sand_iron.png'),
                         load_image('sand_gold.png'),
                         load_image('sand_diamond.png')]
                bg, x_tiles, y_tiles = background(screen_size, tiles, True,
                                                  (90, 4, 3, 2, 1))

                bg_drawn = True

            render_cursor = False
            x, y = pygame.mouse.get_pos()
            mouse_in_area = (board.left <= x <= board.left + board.width *
                             board.cell_size and board.top <= y <= board.top +
                             board.height * board.cell_size)

            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(False)

                if mouse_in_area:
                    render_cursor = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if home_button_2.update(event):
                    mode = 1
                    bg_drawn = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if board.count and mouse_in_area:
                        board.get_click(event.pos, table, particles_group)

            # Drawing background
            for y in range(y_tiles - 1, -1, -1):
                for x in range(x_tiles):
                    screen.blit(bg[y][x], (x * 120, y * 120))

            # Working with text
            dig_count.render(board.count)
            money.render()

            if not board.count:

                if not calculated:
                    for key in table.resources:
                        if table.resources[key] != 0:
                            table.rendering.append(key)
                    table.render_count = len(table.rendering)
                    calculated = True

                table.render()
                table.update()

                dig_count.update()

            board.render(screen)

            particles_group.update(screen_rect)

            dig_menu.draw(screen)
            super_group.draw(screen)
            particles_group.draw(screen)

            cursor.update(not render_cursor)
            pickaxe_cursor.update(render_cursor)

            pygame.display.flip()

        if mode == 3:
            if not bg_drawn:
                # Loading background
                x_tiles, y_tiles = background(screen_size, rand=False)
                bg = load_image('bricks.png')

                bg_drawn = True

            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(False)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if home_button_3.update(event):
                    mode = 1
                    bg_drawn = False

                if storage_button.update(event):
                    pass

                if powerup_button.update(event):
                    pass

            # Drawing background
            for x in range(x_tiles):
                for y in range(y_tiles):
                    screen.blit(bg, (x * 120, y * 120))

            money.render()

            workshop_menu.draw(screen)

            # Cursor render
            super_group.draw(screen)
            cursor.update(True)

            pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    # try:
    main()
    sys.exit()
    # except Exception:
    #     print('Sorry, something went wrong!')
    #     terminate()
