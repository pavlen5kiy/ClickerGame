import json
import random
import sys
import math

import pygame
from board import Board
from image_controller import load_image
from ui import Table, DigCount, PopUpWindow, Settings
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

    pygame.display.set_caption('ClickerGame')

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
    screen, screen_size, screen_rect = screen_init()

    pygame.mouse.set_visible(False)

    pygame.display.flip()

    clock = pygame.time.Clock()

    score = {
        'coins': 9999,
        'gems': 9999,
        'coal': 0,
        'iron': 0,
        'gold': 0,
        'iron nuggets': 0,
        'gold nuggets': 0,
        'melt iron': 0,
        'melt gold': 0,
        'iron ingots': 0,
        'gold ingots': 0,
        'crushing clicks': ['value', 'level', 'price', 'value change',
                            'price change', 'max_level']
    }

    try:
        with open('score.txt') as score_file:
            score = json.load(score_file)
    except:
        print('No file created yet')

    mode = 1
    money = Money(screen, screen_size, score)
    money.coins = score['coins']
    money.gems = score['gems']

    cast_image = load_image("cast.png")
    db_image = load_image("map.png")
    wh_image = load_image("workshop.png")
    sell_image = load_image("sell.png")
    close_image = load_image("close.png")
    home_image = load_image("home.png")
    storage_image = load_image("chest.png")
    powerup_image = load_image("powerup.png")
    crush_image = load_image("crush.png")
    melt_image = load_image("bucket.png")
    settings_image = load_image('settings.png')
    exchange_image = load_image('exchange.png')

    super_group = pygame.sprite.Group()
    main_menu = pygame.sprite.Group()
    dig_menu = pygame.sprite.Group()
    workshop_menu = pygame.sprite.Group()
    particles_group = pygame.sprite.Group()

    powerup_window = PopUpWindow(screen, screen_size, 'POWERUPS', {'a': 0})
    storage_window = PopUpWindow(screen, screen_size, 'RESOURCES',
                                 {k: score[k] for k in
                                  list(score.keys())[2:11]})
    settings_window = Settings(screen, screen_size, 'SETTINGS', 'You idiot')

    popup_windows = [powerup_window, storage_window, settings_window]

    # MENU

    # Sprites
    cursor_image = load_image("cursor.png")
    cursor = Cursor(cursor_image, super_group)

    dig_button = Button(db_image, load_image('map_highlited.png'),
                        (
                            screen_size[0] // 4 - db_image.get_width() // 2,
                            screen_size[1] // 2 - db_image.get_height() // 2),
                        main_menu)

    workshop_button = Button(wh_image,
                             load_image('workshop_highlited.png'),
                             (
                                 screen_size[0] // 2 + screen_size[
                                     0] // 4 - wh_image.get_width() // 2,
                                 screen_size[
                                     1] // 2 - wh_image.get_height() // 2),
                             main_menu)

    sell_button = Button(sell_image,
                         load_image('sell_highlited.png'),
                         (
                             screen_size[0] // 2 - sell_image.get_width() // 2,
                             screen_size[
                                 1] // 3 * 2 - sell_image.get_height() // 2),
                         main_menu)

    close_button = Button(close_image,
                          load_image('close_highlited.png'),
                          (10, screen_size[1] - close_image.get_height() - 10),
                          main_menu)

    settings_button = Button(settings_image,
                             load_image('settings_highlited.png'),
                             (screen_size[0] - settings_image.get_width() - 10,
                              screen_size[
                                  1] - settings_image.get_height() - 10),
                             main_menu)

    exchage_button = Button(exchange_image,
                            load_image('exchange_highlited.png'),
                            (10, 10), main_menu)

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if close_button.update(event):
                    running = False

                if dig_button.update(event):
                    if score['coins'] - 100 < 0:
                        print('not enough coins')
                    else:
                        score['coins'] -= 100

                        # Board
                        size = 7, 7
                        board = Board(score, *size)
                        cell_size = 120
                        left = screen_size[
                                   0] // 2 - board.width * cell_size // 2
                        top = screen_size[
                                  1] // 2 - board.height * cell_size // 2
                        board.set_view(left, top, cell_size)

                        width, height = screen_size

                        calculated = False

                        # Ui
                        table = Table(screen, screen_size)
                        dig_count = DigCount(screen, screen_size)

                        # Sprites
                        pickaxe_cursor = Cursor(
                            load_image("pickaxe_cursor.png"),
                            dig_menu)

                        home_button_2 = Button(home_image,
                                               load_image(
                                                   'home_highlited.png'),
                                               (10, screen_size[
                                                   1] - home_image.get_height() - 10),
                                               dig_menu)
                        home_button_2.kill()

                        for window in popup_windows:
                            window.show = False

                        mode = 2
                        bg_drawn = False

                if workshop_button.update(event):
                    # WORKSHOP
                    home_button_3 = Button(home_image,
                                           load_image('home_highlited.png'),
                                           (10, screen_size[
                                               1] - home_image.get_height() - 10),
                                           workshop_menu)

                    storage_button = Button(storage_image,
                                            load_image('chest_highlited.png'),
                                            (screen_size[
                                                 0] - storage_image.get_width() - 10,
                                             screen_size[
                                                 1] - storage_image.get_height() - 10),
                                            workshop_menu)

                    powerup_button = Button(powerup_image,
                                            load_image(
                                                'powerup_highlited.png'),
                                            (screen_size[
                                                 0] - powerup_image.get_width() - powerup_image.get_width() - 20,
                                             screen_size[
                                                 1] - powerup_image.get_height() - 10),
                                            workshop_menu)

                    crush_button = Button(crush_image,
                                          load_image('crush_highlited.png'),
                                          (screen_size[
                                               0] // 4 - crush_image.get_width() // 2,
                                           screen_size[
                                               1] // 2 - crush_image.get_height() // 2),
                                          workshop_menu)

                    melt_button = Button(melt_image,
                                         load_image('bucket_highlited.png'),
                                         (screen_size[
                                              0] // 2 - melt_image.get_width() // 2,
                                          screen_size[
                                              1] // 2 - melt_image.get_height() // 2),
                                         workshop_menu)

                    cast_button = Button(cast_image,
                                         load_image('cast_highlited.png'),
                                         (screen_size[0] // 2 + screen_size[
                                             0] // 4 - cast_image.get_width() // 2,
                                          screen_size[
                                              1] // 2 - cast_image.get_height() // 2),
                                         workshop_menu)

                    for window in popup_windows:
                        window.show = False

                    mode = 3
                    bg_drawn = False

                if sell_button.update(event):
                    pass

                if settings_button.update(event):
                    settings_window.show = not settings_window.show
                    if settings_window.show:
                        for window in popup_windows:
                            if window is not settings_window:
                                window.show = False

                if exchage_button.update(event):
                    if score['gems'] - 20 < 0:
                        print('not enough gems')
                    else:
                        score['gems'] -= 20
                        score['coins'] += 500

            # Drawing background
            for x in range(x_tiles):
                for y in range(y_tiles):
                    screen.blit(bg, (x * 120, y * 120))

            money.render()

            main_menu.draw(screen)

            settings_window.render()

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

            if mouse_in_area:
                render_cursor = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if not board.count:
                    if home_button_2.update(event):
                        for sprite in dig_menu.sprites():
                            sprite.kill()

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
                    home_button_2 = Button(home_image,
                                           load_image('home_highlited.png'),
                                           (10, screen_size[
                                               1] - home_image.get_height() - 10),
                                           dig_menu)

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if home_button_3.update(event):
                    for sprite in workshop_menu.sprites():
                        sprite.kill()

                    for window in popup_windows:
                        window.show = False

                    mode = 1
                    bg_drawn = False

                if crush_button.update(event):
                    pass

                if melt_button.update(event):
                    pass

                if storage_button.update(event):
                    storage_window.data = {k: score[k] for k in
                                           list(score.keys())[2:11]}
                    storage_window.show = not storage_window.show
                    if storage_window.show:
                        for window in popup_windows:
                            if window is not storage_window:
                                window.show = False

                if powerup_button.update(event):
                    powerup_window.show = not powerup_window.show
                    if powerup_window.show:
                        for window in popup_windows:
                            if window is not powerup_window:
                                window.show = False

                if cast_button.update(event):
                    pass

            # Drawing background
            for x in range(x_tiles):
                for y in range(y_tiles):
                    screen.blit(bg, (x * 120, y * 120))

            money.render()

            workshop_menu.draw(screen)

            for window in popup_windows:
                window.render()

            # Cursor render
            super_group.draw(screen)
            cursor.update(True)

            pygame.display.flip()

    with open('score.txt', 'w') as score_file:
        json.dump(score, score_file)

    pygame.quit()


if __name__ == '__main__':
    # try:
    main()
    sys.exit()
    # except Exception:
    #     print('Sorry, something went wrong!')
    #     terminate()
