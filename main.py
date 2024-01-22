import json
import random
import sys
import math

import pygame
from board import *
from image_controller import *
from ui import *
from money import *
from sprite_controller import *
from test import Crushing


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


def menu_change(closing_group, popup_windows, kill_previous=True):
    if kill_previous:
        for sprite in closing_group.sprites():
            sprite.kill()

    for window in popup_windows:
        window.show = False


def draw_background(screen, bg, x_tiles, y_tiles):
    # Drawing background
    for x in range(x_tiles):
        for y in range(y_tiles):
            screen.blit(bg, (x * 120, y * 120))


def main():
    pygame.init()
    screen, screen_size, screen_rect = screen_init()

    pygame.mouse.set_visible(False)

    pygame.display.flip()

    clock = pygame.time.Clock()

    score = {
        'coins': 1000,
        'gems': 100,
        'coal': 0,
        'iron': 0,
        'gold': 0,
        'iron nuggets': 0,
        'gold nuggets': 0,
        'melt iron': 0,
        'melt gold': 0,
        'iron ingots': 0,
        'gold ingots': 0,
        'digging': [5, [5, 10, 20, 35, 49], [0, 200, 600, 1000, 1500], 'clk'],
        'crushing': [10, [10, 7, 5, 3], [0, 200, 600, 1000], 'clk'],
        'melting time': [10, [10, 7, 5, 3], [0, 500, 1000, 2000], 'sec'],
        'exchange gems': [20, [20, 15, 10], [0, 10000, 20000], 'gem']
    }

    maps = {
        'Wastelands': [3, 100],
        'Hills': [4, 200],
        'Lake': [5, 500],
        'Canyon': [6, 700],
        'Mountains': [7, 1000]
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
    back_image = load_image('back.png')
    ok_image = load_image('ok.png')
    gold_ingots_image = load_image('gold_ingots.png')
    iron_ingots_image = load_image('iron_ingots.png')
    window_image = load_image('window.png')
    gold_ore_image = load_image('gold_ore.png')
    iron_ore_image = load_image('iron_ore.png')
    gold_nugget_image = load_image('gold_nugget.png')
    iron_nugget_image = load_image('iron_nugget.png')
    melt_gold_image = load_image('melt_gold.png')
    melt_iron_image = load_image('melt_iron.png')

    super_group = pygame.sprite.Group()
    main_menu = pygame.sprite.Group()
    dig_menu = pygame.sprite.Group()
    workshop_menu = pygame.sprite.Group()
    particles_group = pygame.sprite.Group()
    sell_menu = pygame.sprite.Group()
    crushing_menu = pygame.sprite.Group()
    melting_menu = pygame.sprite.Group()
    casting_menu = pygame.sprite.Group()
    powerup_buttons = pygame.sprite.Group()
    map_buttons = pygame.sprite.Group()

    powerup_window = PopUpWindow(screen, screen_size, 'UPGRADES', {k: f'{score[k][-1]} {score[k][0]}' for k in
                                  list(score.keys())[11:]})
    storage_window = PopUpWindow(screen, screen_size, 'RESOURCES',
                                 {k: score[k] for k in
                                  list(score.keys())[2:11]})
    settings_window = Settings(screen, screen_size, 'SETTINGS', 'You idiot')
    maps_window = PopUpWindow(screen, screen_size, 'MAPS',
                                 {k: f'{maps[k][0]}x{maps[k][0]}' for k in
                                  list(maps.keys())})

    status_bar = StatusBar(screen, screen_size)

    popup_windows = [powerup_window, storage_window, settings_window, maps_window]

    powerup_buttons_list = []
    for i in range(4):
        powerup_buttons_list.append(Button(load_image('arrow.png'),
                                   'arrow.png',
                                   (screen_size[0] // 2 + window_image.get_width() // 2 - 67,
                                    screen_size[1] // 2 - window_image.get_height() // 2 + 80 + 60 * i)))

    map_buttons_list = []
    for i in range(5):
        map_buttons_list.append(Button(load_image('arrow.png'),
                                           'arrow.png',
                                           (screen_size[
                                                0] // 2 + window_image.get_width() // 2 - 67,
                                            screen_size[
                                                1] // 2 - window_image.get_height() // 2 + 80 + 60 * i)))

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

                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/coralchorus.mp3')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)

                status_bar.time_count = 0
                choosen = False

                bg_drawn = True

            for event in pygame.event.get():
                if not any([window.show for window in popup_windows]):
                    if event.type == pygame.QUIT:
                        running = False

                    if close_button.update(event):
                        running = False

                    if dig_button.update(event):
                        maps_window.show = True
                        current = 0

                        map = list(maps.keys())[current]
                        coins = maps[map][1]
                        msg = f"Press [E]. Price: {coins}"

                        status_bar.time_count = status_bar.default
                        status_bar.text = msg

                        map_buttons = pygame.sprite.Group()
                        map_buttons.add(map_buttons_list[current])

                    if workshop_button.update(event):
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('data/saxygroove.mp3')
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)

                        # WORKSHOP
                        home_button_3 = Button(home_image,
                                               load_image(
                                                   'home_highlited.png'),
                                               (10, screen_size[
                                                   1] - home_image.get_height() - 10),
                                               workshop_menu)

                        storage_button = Button(storage_image,
                                                load_image(
                                                    'chest_highlited.png'),
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
                                              load_image(
                                                  'crush_highlited.png'),
                                              (screen_size[
                                                   0] // 4 - crush_image.get_width() // 2,
                                               screen_size[
                                                   1] // 2 - crush_image.get_height() // 2),
                                              workshop_menu)

                        melt_button = Button(melt_image,
                                             load_image(
                                                 'bucket_highlited.png'),
                                             (screen_size[
                                                  0] // 2 - melt_image.get_width() // 2,
                                              screen_size[
                                                  1] // 2 - melt_image.get_height() // 2),
                                             workshop_menu)

                        cast_button = Button(cast_image,
                                             load_image('cast_highlited.png'),
                                             (
                                                 screen_size[0] // 2 +
                                                 screen_size[
                                                     0] // 4 - cast_image.get_width() // 2,
                                                 screen_size[
                                                     1] // 2 - cast_image.get_height() // 2),
                                             workshop_menu)

                        menu_change(main_menu, popup_windows, False)
                        mode = 3
                        bg_drawn = False

                    if sell_button.update(event):
                        # SELL

                        if not score['gold ingots'] and not score['iron ingots']:
                            status_bar.time_count = status_bar.default
                            status_bar.text = 'You have nothing to sell!'
                        else:
                            home_button_7 = Button(home_image,
                                                   load_image(
                                                       'home_highlited.png'),
                                                   (10, screen_size[
                                                       1] - home_image.get_height() - 10),
                                                   sell_menu)

                            gold_button_7 = Button(gold_ingots_image,
                                                 load_image(
                                                     'gold_ingots_highlited.png'),
                                                 (screen_size[
                                                      0] // 2 + screen_size[
                                                      0] // 4 - gold_ingots_image.get_width() // 2,
                                                  screen_size[
                                                      1] // 2 - gold_ingots_image.get_height() // 2),
                                                 sell_menu)

                            iron_button_7 = Button(iron_ingots_image,
                                                 load_image(
                                                     'iron_ingots_highlited.png'),
                                                 (screen_size[
                                                      0] // 4 - iron_ingots_image.get_width() // 2,
                                                  screen_size[
                                                      1] // 2 - iron_ingots_image.get_height() // 2),
                                                 sell_menu)

                            timer = Timer(-1, screen, screen_size)

                            menu_change(main_menu, popup_windows, False)
                            mode = 7
                            bg_drawn = False

                    if settings_button.update(event):
                        settings_window.show = True
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load('data/whistle.mp3')
                        pygame.mixer.music.set_volume(0.5)
                        pygame.mixer.music.play(-1)

                    if exchage_button.update(event):
                        if score['gems'] - score['exchange gems'][0] < 0:
                            status_bar.time_count = status_bar.default
                            status_bar.text = 'Not enough gems!'
                        else:
                            score['gems'] -= score['exchange gems'][0]
                            score['coins'] += 500

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if any([window.show for window in popup_windows]):
                            for window in popup_windows:
                                window.show = False

                            pygame.mixer.music.stop()
                            pygame.mixer.music.load('data/coralchorus.mp3')
                            pygame.mixer.music.set_volume(0.5)
                            pygame.mixer.music.play(-1)

                            status_bar.time_count = 0
                    if event.key == pygame.K_c:
                        if not any([window.show for window in popup_windows]):
                            if score['gems'] - score['exchange gems'][0] < 0:
                                status_bar.time_count = status_bar.default
                                status_bar.text = 'Not enough gems!'
                            else:
                                score['gems'] -= score['exchange gems'][0]
                                score['coins'] += 500
                    if event.key == pygame.K_q:
                        running = False

                    if maps_window.show:
                        map = list(maps.keys())[current]
                        coins = maps[map][1]
                        msg = f"Press [E]. Price: {coins}"

                        if event.key == pygame.K_DOWN:
                            if 0 <= current + 1 <= len(map_buttons_list) - 1:
                                current += 1
                                map_buttons = pygame.sprite.Group()
                                map_buttons.add(map_buttons_list[current])

                                map = list(maps.keys())[current]

                                coins = maps[map][1]
                                msg = f"Press [E]. Price: {coins}"

                                status_bar.time_count = status_bar.default
                                status_bar.text = msg
                            else:
                                current = 0
                                map_buttons = pygame.sprite.Group()
                                map_buttons.add(map_buttons_list[current])

                                map = list(maps.keys())[current]

                                coins = maps[map][1]
                                msg = f"Press [E]. Price: {coins}"

                                status_bar.time_count = status_bar.default
                                status_bar.text = msg
                        if event.key == pygame.K_UP:
                            if 0 <= current - 1 <= len(map_buttons_list) - 1:
                                current -= 1
                                map_buttons = pygame.sprite.Group()
                                map_buttons.add(map_buttons_list[current])

                                map = list(maps.keys())[current]

                                coins = maps[map][1]
                                msg = f"Press [E]. Price: {coins}"

                                status_bar.time_count = status_bar.default
                                status_bar.text = msg
                            else:
                                current = len(map_buttons_list) - 1
                                map_buttons = pygame.sprite.Group()
                                map_buttons.add(map_buttons_list[current])

                                map = list(maps.keys())[current]

                                coins = maps[map][1]
                                msg = f"Press [E]. Price: {coins}"

                                status_bar.time_count = status_bar.default
                                status_bar.text = msg
                        if event.key == pygame.K_e:
                            status_bar.time_count = status_bar.default
                            map = list(maps.keys())[current]
                            size = maps[map][0], maps[map][0]
                            coins = maps[map][1]
                            if score['coins'] - coins >= 0:
                                score['coins'] -= coins
                                choosen = True
                            else:
                                status_bar.text = f"Not enough coins!"

            if choosen:
                # Board
                board = Board(score, *size)
                board.count = score['digging'][0]
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

                menu_change(main_menu, popup_windows, False)
                mode = 2
                bg_drawn = False

            draw_background(screen, bg, x_tiles, y_tiles)

            money.render()

            main_menu.draw(screen)

            for window in popup_windows:
                window.render()

            if maps_window.show:
                status_bar.time_count = status_bar.default
                maps_window.data = {k: f'{maps[k][0]}x{maps[k][0]}' for k in list(maps.keys())}
                map_buttons.draw(screen)

            status_bar.render()

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

                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/burzum.mp3')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)

                status_bar.time_count = 0
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

                if not board.count or board.width**2 == len(board.clicked):
                    if home_button_2.update(
                            event) or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        menu_change(dig_menu, popup_windows)
                        mode = 1
                        bg_drawn = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if board.count and mouse_in_area:
                        board.get_click(event.pos, table, particles_group)

            # Drawing background. It's specific, so don't use function
            for y in range(y_tiles - 1, -1, -1):
                for x in range(x_tiles):
                    screen.blit(bg[y][x], (x * 120, y * 120))

            # Working with text
            dig_count.render(board.count)
            money.render()

            if not board.count or board.width**2 == len(board.clicked):

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

                status_bar.time_count = 0
                bg_drawn = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if not any([window.show for window in popup_windows]):
                    if home_button_3.update(event):
                        menu_change(workshop_menu, popup_windows)
                        mode = 1
                        bg_drawn = False

                    if crush_button.update(event):
                        back_button_4 = Button(back_image,
                                               load_image(
                                                   'back_highlited.png'),
                                               (10, screen_size[
                                                   1] - home_image.get_height() - 10),
                                               crushing_menu)

                        gold_button_4 = Button(gold_ore_image,
                                               load_image(
                                                   'gold_ore_highlited.png'),
                                               (screen_size[
                                                    0] // 2 + screen_size[
                                                    0] // 4 - gold_ore_image.get_width() // 2,
                                                screen_size[
                                                    1] // 2 - gold_ore_image.get_height() // 2),
                                               crushing_menu)

                        iron_button_4 = Button(iron_ore_image,
                                               load_image(
                                                   'iron_ore_highlited.png'),
                                               (screen_size[
                                                    0] // 4 - iron_ore_image.get_width() // 2,
                                                screen_size[
                                                    1] // 2 - iron_ore_image.get_height() // 2),
                                               crushing_menu)

                        pickaxe_cursor = Cursor(
                            load_image("pickaxe_cursor.png"),
                            crushing_menu)

                        menu_change(workshop_menu, popup_windows, False)
                        mode = 4
                        bg_drawn = False

                    if melt_button.update(event):
                        back_button_5 = Button(back_image,
                                               load_image(
                                                   'back_highlited.png'),
                                               (10, screen_size[
                                                   1] - home_image.get_height() - 10),
                                               melting_menu)

                        gold_button_5 = Button(gold_nugget_image,
                                               load_image(
                                                   'gold_nugget_highlited.png'),
                                               (screen_size[
                                                    0] // 2 + screen_size[
                                                    0] // 4 - gold_nugget_image.get_width() // 2,
                                                screen_size[
                                                    1] // 2 - gold_nugget_image.get_height() // 2),
                                               melting_menu)

                        iron_button_5 = Button(iron_nugget_image,
                                               load_image(
                                                   'iron_nugget_highlited.png'),
                                               (screen_size[
                                                    0] // 4 - iron_nugget_image.get_width() // 2,
                                                screen_size[
                                                    1] // 2 - iron_nugget_image.get_height() // 2 - 70),
                                               melting_menu)

                        menu_change(workshop_menu, popup_windows, False)
                        mode = 5
                        bg_drawn = False

                    if cast_button.update(event):
                        back_button_6 = Button(back_image,
                                               load_image(
                                                   'back_highlited.png'),
                                               (10, screen_size[
                                                   1] - home_image.get_height() - 10),
                                               casting_menu)

                        gold_button_6 = Button(melt_gold_image,
                                               load_image(
                                                   'melt_gold_highlited.png'),
                                               (screen_size[
                                                    0] // 2 + screen_size[
                                                    0] // 4 - melt_gold_image.get_width() // 2,
                                                screen_size[
                                                    1] // 2 - melt_gold_image.get_height() // 2),
                                               casting_menu)

                        iron_button_6 = Button(melt_iron_image,
                                               load_image(
                                                   'melt_iron_highlited.png'),
                                               (screen_size[
                                                    0] // 4 - melt_iron_image.get_width() // 2,
                                                screen_size[
                                                    1] // 2 - melt_iron_image.get_height() // 2),
                                               casting_menu)

                        menu_change(workshop_menu, popup_windows, False)
                        mode = 6
                        bg_drawn = False

                    if storage_button.update(event):
                        storage_window.data = {k: score[k] for k in
                                               list(score.keys())[2:11]}
                        storage_window.show = True

                    if powerup_button.update(event):
                        powerup_window.show = True
                        current = 0

                        upgrade = list(score.keys())[11:][current]
                        next = score[upgrade][1].index(score[upgrade][0]) + 1
                        if next <= len(score[upgrade][1]) - 1:
                            coins = score[upgrade][2][
                                score[upgrade][1].index(score[upgrade][0]) + 1]
                            msg = f"Press [U]. Price: {coins}"
                        else:
                            msg = "You've reached your max!"

                        status_bar.time_count = status_bar.default
                        status_bar.text = msg

                        powerup_buttons = pygame.sprite.Group()
                        powerup_buttons.add(powerup_buttons_list[current])

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if any([window.show for window in popup_windows]):
                            for window in popup_windows:
                                window.show = False
                            status_bar.time_count = 0
                        else:
                            menu_change(workshop_menu, popup_windows)
                            mode = 1
                            bg_drawn = False

                    if powerup_window.show:
                        upgrade = list(score.keys())[11:][current]
                        next = score[upgrade][1].index(score[upgrade][0]) + 1
                        if next <= len(score[upgrade][1]) - 1:
                            coins = score[upgrade][2][score[upgrade][1].index(score[upgrade][0]) + 1]
                            msg = f"Press [U]. Price: {coins}"
                        else:
                            msg = "You've reached your max!"

                        if event.key == pygame.K_DOWN:
                            if 0 <= current + 1 <= len(powerup_buttons_list) - 1:
                                current += 1
                                powerup_buttons = pygame.sprite.Group()
                                powerup_buttons.add(powerup_buttons_list[current])

                                upgrade = list(score.keys())[11:][current]
                                next = score[upgrade][1].index(
                                    score[upgrade][0]) + 1
                                if next <= len(score[upgrade][1]) - 1:
                                    coins = score[upgrade][2][
                                        score[upgrade][1].index(
                                            score[upgrade][0]) + 1]
                                    msg = f"Press [U]. Price: {coins}"
                                else:
                                    msg = "You've reached your max!"

                                status_bar.time_count = status_bar.default
                                status_bar.text = msg
                            else:
                                current = 0
                                powerup_buttons = pygame.sprite.Group()
                                powerup_buttons.add(powerup_buttons_list[current])

                                upgrade = list(score.keys())[11:][current]
                                next = score[upgrade][1].index(
                                    score[upgrade][0]) + 1
                                if next <= len(score[upgrade][1]) - 1:
                                    coins = score[upgrade][2][
                                        score[upgrade][1].index(
                                            score[upgrade][0]) + 1]
                                    msg = f"Press [U]. Price: {coins}"
                                else:
                                    msg = "You've reached your max!"

                                status_bar.time_count = status_bar.default
                                status_bar.text = msg
                        if event.key == pygame.K_UP:
                            if 0 <= current - 1 <= len(powerup_buttons_list) - 1:
                                current -= 1
                                powerup_buttons = pygame.sprite.Group()
                                powerup_buttons.add(powerup_buttons_list[current])

                                upgrade = list(score.keys())[11:][current]
                                next = score[upgrade][1].index(
                                    score[upgrade][0]) + 1
                                if next <= len(score[upgrade][1]) - 1:
                                    coins = score[upgrade][2][
                                        score[upgrade][1].index(
                                            score[upgrade][0]) + 1]
                                    msg = f"Press [U]. Price: {coins}"
                                else:
                                    msg = "You've reached your max!"

                                status_bar.time_count = status_bar.default
                                status_bar.text = msg
                            else:
                                current = len(powerup_buttons_list) - 1
                                powerup_buttons = pygame.sprite.Group()
                                powerup_buttons.add(powerup_buttons_list[current])

                                upgrade = list(score.keys())[11:][current]
                                next = score[upgrade][1].index(
                                    score[upgrade][0]) + 1
                                if next <= len(score[upgrade][1]) - 1:
                                    coins = score[upgrade][2][
                                        score[upgrade][1].index(
                                            score[upgrade][0]) + 1]
                                    msg = f"Press [U]. Price: {coins}"
                                else:
                                    msg = "You've reached your max!"

                                status_bar.time_count = status_bar.default
                                status_bar.text = msg
                        if event.key == pygame.K_u:
                                status_bar.time_count = status_bar.default
                                if next <= len(score[upgrade][1]) - 1:
                                    coins = score[upgrade][2][score[upgrade][1].index(score[upgrade][0]) + 1]
                                    if score['coins'] - coins >= 0:
                                        score[upgrade][0] = score[upgrade][1][next]
                                        score['coins'] -= coins
                                        status_bar.text = f"You've paid {coins} coins!"
                                    else:
                                        status_bar.text = f"Not enough coins!"
                                else:
                                    status_bar.text = "You've reached your max!"

            # Drawing background
            draw_background(screen, bg, x_tiles, y_tiles)

            money.render()

            workshop_menu.draw(screen)

            for window in popup_windows:
                window.render()

            if powerup_window.show:
                status_bar.time_count = status_bar.default
                powerup_window.data = {k: f'{score[k][-1]} {score[k][0]}' for k in list(score.keys())[11:]}
                powerup_buttons.draw(screen)

            status_bar.render()

            # Cursor render
            super_group.draw(screen)
            cursor.update(True)

            pygame.display.flip()

        if mode == 4:
            if not bg_drawn:
                # Loading background
                x_tiles, y_tiles = background(screen_size, rand=False)
                bg = load_image('bricks.png')

                particles_group = pygame.sprite.Group()
                started = False
                current = 0
                clicks = 0

                render_cursor = False
                status_bar.time_count = 0
                bg_drawn = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if back_button_4.update(event) or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    menu_change(crushing_menu, popup_windows)
                    mode = 3
                    bg_drawn = False
                    particles_group = pygame.sprite.Group()

                if not current:
                    if gold_button_4.update(event) or iron_button_4.update(event):
                        status_bar.time_count = 0
                        if gold_button_4.update(event):
                            if score['gold']:
                                current = 2
                                chosen = score['gold']
                                got = score['gold nuggets']
                                gold_button_4.kill()
                                iron_button_4.kill()
                                render_cursor = True
                            else:
                                status_bar.time_count = status_bar.default
                                status_bar.text = "You don't have any gold ore!"
                        if iron_button_4.update(event):
                            if score['iron']:
                                current = 1
                                chosen = score['iron']
                                got = score['iron nuggets']
                                gold_button_4.kill()
                                iron_button_4.kill()
                                render_cursor = True
                            else:
                                status_bar.time_count = status_bar.default
                                status_bar.text = "You don't have any iron ore!"

                elif current == 1:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if score['iron'] != 0:
                            create_particles(pygame.mouse.get_pos(),
                                             generate_particles(
                                                 'stone_iron_particle.png'),
                                             20,
                                             particles_group)
                            clicks += 1
                            if clicks == score['crushing'][0]:
                                score['iron'] -= 1
                                score['iron nuggets'] += random.randrange(1, 7)
                                clicks = 0
                                create_particles(pygame.mouse.get_pos(),
                                                 generate_particles(
                                                     'iron_particle.png'),
                                                 20,
                                                 particles_group)

                elif current == 2:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if score['gold'] != 0:
                            create_particles(pygame.mouse.get_pos(),
                                             generate_particles(
                                                 'stone_gold_particle.png'),
                                             20,
                                             particles_group)
                            clicks += 1
                            if clicks == score['crushing'][0]:
                                score['gold'] -= 1
                                score['gold nuggets'] += random.randrange(1, 3)
                                clicks = 0
                                create_particles(pygame.mouse.get_pos(),
                                                 generate_particles(
                                                     'gold_particle.png'),
                                                 20,
                                                 particles_group)

            draw_background(screen, bg, x_tiles, y_tiles)

            if not current:
                iron_amount = pygame.font.Font(None, 100).render(
                    f"x {score['iron']}", True, 'white')
                screen.blit(iron_amount, (screen_size[
                                                      0] // 4 - iron_amount.get_width() // 2,
                                                  screen_size[
                                                      1] // 2 + iron_ingots_image.get_height() // 2 + 50))

                gold_amount = pygame.font.Font(None, 100).render(
                    f"x {score['gold']}", True, 'white')
                screen.blit(gold_amount, (screen_size[
                                              0] // 2 + screen_size[0] // 4 - gold_amount.get_width() // 2,
                                          screen_size[
                                              1] // 2 + gold_ingots_image.get_height() // 2 + 50))
            else:
                if current == 1:
                    chosen = score['iron']
                    got = score['iron nuggets']
                    ct = 'Iron'
                    gt = 'Iron nuggets'
                    screen.blit(iron_ore_image, (screen_size[0] // 2 - iron_ore_image.get_width() // 2,
                                                 (screen_size[1] // 2 - iron_ore_image.get_height() // 2)))
                elif current == 2:
                    chosen = score['gold']
                    got = score['gold nuggets']
                    ct = 'Gold'
                    gt = 'Gold nuggets'
                    screen.blit(gold_ore_image, (
                    screen_size[0] // 2 - gold_ore_image.get_width() // 2,
                    (screen_size[1] // 2 - gold_ore_image.get_height() // 2)))

                chosen_text = pygame.font.Font(None, 100).render(
                    f"{ct} x {chosen}", True, 'white')
                screen.blit(chosen_text, (screen_size[
                                              0] // 4 - chosen_text.get_width() // 2,
                                          screen_size[
                                              1] // 2 + iron_ingots_image.get_height() // 2 + 50))

                got_text = pygame.font.Font(None, 100).render(
                    f"{gt} x {got}", True, 'white')
                screen.blit(got_text, (screen_size[
                                              0] // 2 + screen_size[
                                              0] // 4 - got_text.get_width() // 2,
                                          screen_size[
                                              1] // 2 + gold_ingots_image.get_height() // 2 + 50))

            crushing_menu.draw(screen)

            status_bar.render()

            particles_group.draw(screen)
            particles_group.update(screen_rect)

            super_group.draw(screen)
            cursor.update(not render_cursor)
            pickaxe_cursor.update(render_cursor)

            pygame.display.flip()

        if mode == 5:
            if not bg_drawn:
                # Loading background
                x_tiles, y_tiles = background(screen_size, rand=False)
                bg = load_image('bricks.png')

                timer = Timer(-1, screen, screen_size)
                time_count = 0
                started = False
                current = 0

                status_bar.time_count = 0
                bg_drawn = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if back_button_5.update(
                        event) or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    menu_change(melting_menu, popup_windows)
                    mode = 3
                    bg_drawn = False

                if not current:
                    if gold_button_5.update(event) or iron_button_5.update(
                            event):
                        if score['coal']:
                            time_count = 0
                            status_bar.time_count = 0
                            if gold_button_5.update(event):
                                if score['gold nuggets']:
                                    current = 2

                                    if score['coal'] >= score['gold nuggets']:
                                        timer.seconds = score['melting time'][0] * score['gold nuggets']
                                    else:
                                        timer.seconds = score['melting time'][0] * score['coal']

                                    gold_button_5.kill()
                                    iron_button_5.kill()
                                else:
                                    status_bar.time_count = status_bar.default
                                    status_bar.text = "You don't have any gold nuggets!"

                            if iron_button_5.update(event):
                                if score['iron nuggets']:
                                    current = 1

                                    if score['coal'] >= score['iron nuggets']:
                                        timer.seconds = score['melting time'][0] * score['iron nuggets']
                                    else:
                                        timer.seconds = score['melting time'][0] * score['coal']

                                    gold_button_5.kill()
                                    iron_button_5.kill()
                                else:
                                    status_bar.time_count = status_bar.default
                                    status_bar.text = "You don't have any iron nuggets!"
                        else:
                            status_bar.time_count = status_bar.default
                            status_bar.text = "You don't have any coal!"

            draw_background(screen, bg, x_tiles, y_tiles)

            if not current:
                iron_amount = pygame.font.Font(None, 100).render(
                    f"x {score['iron nuggets']}", True, 'white')
                screen.blit(iron_amount, (screen_size[
                                                      0] // 4 - iron_amount.get_width() // 2,
                                                  screen_size[
                                                      1] // 2 + iron_ingots_image.get_height() // 2 + 50))

                gold_amount = pygame.font.Font(None, 100).render(
                    f"x {score['gold nuggets']}", True, 'white')
                screen.blit(gold_amount, (screen_size[
                                              0] // 2 + screen_size[0] // 4 - gold_amount.get_width() // 2,
                                          screen_size[
                                              1] // 2 + gold_ingots_image.get_height() // 2 + 50))
            else:
                if not score['coal']:
                    timer.seconds = -1

                if current == 1:
                    chosen = score['iron nuggets']
                    got = score['melt iron']
                    ct = 'Iron nuggets'
                    gt = 'Melt iron'
                    screen.blit(iron_nugget_image, (
                    screen_size[0] // 2 - iron_nugget_image.get_width() // 2,
                    (screen_size[1] // 2 - iron_nugget_image.get_height() // 2)))

                    if score['iron nuggets'] and score['coal']:
                        if timer.seconds > 0:
                            if time_count == 60 * score['melting time'][0] - 1:
                                score['iron nuggets'] -= 1
                                score['coal'] -= 1
                                score['melt iron'] += 1
                                time_count = 0
                            else:
                                time_count += 1
                        if timer.seconds == 0:
                            score['iron nuggets'] -= 1
                            score['coal'] -= 1
                            score['melt iron'] += 1
                            time_count = 0
                    else:
                        status_bar.time_count = status_bar.default
                        status_bar.text = "You're out of resources!"

                elif current == 2:
                    chosen = score['gold nuggets']
                    got = score['melt gold']
                    ct = 'Gold nuggets'
                    gt = 'Melt gold'
                    screen.blit(gold_nugget_image, (
                        screen_size[0] // 2 - gold_nugget_image.get_width() // 2,
                        (screen_size[
                             1] // 2 - gold_nugget_image.get_height() // 2)))

                    if score['gold nuggets'] and score['coal']:
                        if timer.seconds > 0:
                            if time_count == 60 * score['melting time'][0] - 1:
                                score['gold nuggets'] -= 1
                                score['coal'] -= 1
                                score['melt gold'] += 1
                                time_count = 0
                            else:
                                time_count += 1
                        if timer.seconds == 0:
                            score['gold nuggets'] -= 1
                            score['coal'] -= 1
                            score['melt gold'] += 1
                            time_count = 0
                    else:
                        status_bar.time_count = status_bar.default
                        status_bar.text = "You're out of resources!"

                chosen_text = pygame.font.Font(None, 100).render(
                    f"{ct} x {chosen}", True, 'white')
                screen.blit(chosen_text, (screen_size[
                                              0] // 4 - chosen_text.get_width() // 2,
                                          screen_size[
                                              1] // 2 + iron_ingots_image.get_height() // 2 + 50))

                got_text = pygame.font.Font(None, 100).render(
                    f"{gt} x {got}", True, 'white')
                screen.blit(got_text, (screen_size[
                                           0] // 2 + screen_size[
                                           0] // 4 - got_text.get_width() // 2,
                                       screen_size[
                                           1] // 2 + gold_ingots_image.get_height() // 2 + 50))
            melting_menu.draw(screen)

            timer.render()

            status_bar.render()

            super_group.draw(screen)

            cursor.update(True)

            pygame.display.flip()

        if mode == 6:
            if not bg_drawn:
                # Loading background
                x_tiles, y_tiles = background(screen_size, rand=False)
                bg = load_image('bricks.png')

                started = False
                current = 0

                status_bar.time_count = 0
                bg_drawn = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if back_button_6.update(
                        event) or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    menu_change(casting_menu, popup_windows)
                    mode = 3
                    bg_drawn = False

                if not current:
                    if gold_button_6.update(event) or iron_button_6.update(
                            event):
                        status_bar.time_count = 0
                        if gold_button_6.update(event):
                            if score['melt gold'] >= 5:
                                score['gold ingots'] = score['melt gold'] // 5
                                status_bar.time_count = status_bar.default
                                status_bar.text = f"You've got {score['melt gold'] // 5} gold ingots!"
                                score['melt gold'] = score['melt gold'] % 5

                                # current = 2
                                # gold_button_6.kill()
                                # iron_button_6.kill()
                            else:
                                status_bar.time_count = status_bar.default
                                status_bar.text = "You don't have enough melt gold!"
                        if iron_button_6.update(event):
                            if score['melt iron'] >= 5:
                                score['iron ingots'] = score['melt iron'] // 5
                                status_bar.time_count = status_bar.default
                                status_bar.text = f"You've got {score['melt iron'] // 5} iron ingots!"
                                score['melt iron'] = score['melt iron'] % 5

                                # current = 1
                                # gold_button_6.kill()
                                # iron_button_6.kill()
                            else:
                                status_bar.time_count = status_bar.default
                                status_bar.text = "You don't have enough melt iron!"

            draw_background(screen, bg, x_tiles, y_tiles)

            # if not current:
            iron_amount = pygame.font.Font(None, 100).render(
                f"x {score['melt iron']}", True, 'white')
            screen.blit(iron_amount, (screen_size[
                                                  0] // 4 - iron_amount.get_width() // 2,
                                              screen_size[
                                                  1] // 2 + iron_ingots_image.get_height() // 2 + 50))

            gold_amount = pygame.font.Font(None, 100).render(
                f"x {score['melt gold']}", True, 'white')
            screen.blit(gold_amount, (screen_size[
                                          0] // 2 + screen_size[0] // 4 - gold_amount.get_width() // 2,
                                      screen_size[
                                          1] // 2 + gold_ingots_image.get_height() // 2 + 50))

            casting_menu.draw(screen)

            status_bar.render()

            super_group.draw(screen)

            cursor.update(True)

            pygame.display.flip()

        if mode == 7:
            if not bg_drawn:
                # Loading background
                x_tiles, y_tiles = background(screen_size, rand=False)
                bg = load_image('pannels.png')

                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/revolutiondeathsquad.mp3')
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)

                pressed = False
                given = False
                start = False
                started = False
                status_bar.time_count = 0
                set = False
                bg_drawn = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if not started or given:
                    if home_button_7.update(
                            event) or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        if given:
                            score[spend] = 0
                        menu_change(sell_menu, popup_windows)
                        mode = 1
                        bg_drawn = False
                else:
                    home_button_7.kill()

                if gold_button_7.update(event) or iron_button_7.update(event):
                    if not pressed:
                        if gold_button_7.update(event):
                            if score['gold ingots']:
                                spend = 'gold ingots'
                                coins = 500
                                seconds = 5
                                velocity = 10
                                pressed = True
                            else:
                                status_bar.time_count = status_bar.default
                                status_bar.text = "You don't have any gold ingots!"
                        else:
                            if score['iron ingots']:
                                spend = 'iron ingots'
                                coins = 200
                                seconds = 10
                                velocity = 5
                                pressed = True
                            else:
                                status_bar.time_count = status_bar.default
                                status_bar.text = "You don't have any iron ingots!"
                    if pressed:
                        if not started:

                            sell_bar = SellBar((screen_size[0] // 2 - 700,
                                                screen_size[1] // 2 - 30),
                                               sell_menu)

                            sell_slider = SellSlider((sell_bar.rect.x,
                                                      sell_bar.rect.x + sell_bar.image.get_width()),
                                                     (
                                                         sell_bar.rect.x + sell_bar.image.get_width() // 2 - 25,
                                                         screen_size[1] // 2 - 50),
                                                     sell_menu)

                            sell_slider.velocity = velocity

                            if not start:
                                started = True
                                timer.time_count = 60
                                timer.seconds = 3
                                gold_button_7.kill()
                                iron_button_7.kill()

                if start:
                    if timer.seconds != 0:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            sell_slider.velocity *= -1
                            sell_slider.rect.x += velocity * sell_slider.velocity // abs(
                                sell_slider.velocity)

            draw_background(screen, bg, x_tiles, y_tiles)

            sell_menu.draw(screen)
            money.render()

            if timer.seconds == 0 and not start:
                start = True

            if start:
                if not set:
                    timer.seconds = seconds
                    set = True

                if timer.seconds != 0:
                    sell_slider.update()

                    percentage = int((700 - abs(
                        sell_slider.rect.x + sell_slider.image.get_width() // 2 - (
                                sell_bar.rect.x + sell_bar.image.get_width() // 2))) / 700 * 100)

                    output = pygame.font.Font(None, 100).render(
                        str(percentage) + '%',
                        True, 'white')
                    screen.blit(output, (
                    screen_size[0] // 2 - output.get_width() // 2,
                    screen_size[1] // 2 - output.get_height() // 2 - 100))

                else:
                    earned = int(coins * score[spend] * percentage / 100)

                    sell_bar.kill()
                    sell_slider.kill()

                    output = pygame.font.Font(None, 200).render(
                        f'{score[spend]} x {percentage}%',
                        True, 'white')
                    screen.blit(output, (
                    screen_size[0] // 2 - output.get_width() // 2,
                    screen_size[1] // 2 - output.get_height() // 2))

                    message = pygame.font.Font(None, 100).render(
                        f"You've earned {earned} coins!",
                        True, 'white')
                    screen.blit(message, (
                        screen_size[0] // 2 - message.get_width() // 2,
                        screen_size[1] // 2 - output.get_height() // 2 + 150))

                    if not given:
                        score['coins'] += earned
                        sell_menu.add(home_button_7)

                        given = True

            if not started:
                iron_amount = pygame.font.Font(None, 100).render(
                    f"x {score['iron ingots']}", True, 'white')
                screen.blit(iron_amount, (screen_size[
                                                      0] // 4 - iron_amount.get_width() // 2,
                                                  screen_size[
                                                      1] // 2 + iron_ingots_image.get_height() // 2 + 50))

                gold_amount = pygame.font.Font(None, 100).render(
                    f"x {score['gold ingots']}", True, 'white')
                screen.blit(gold_amount, (screen_size[
                                              0] // 2 + screen_size[0] // 4 - gold_amount.get_width() // 2,
                                          screen_size[
                                              1] // 2 + gold_ingots_image.get_height() // 2 + 50))

            timer.render()

            status_bar.render()

            super_group.draw(screen)
            cursor.update(True)

            pygame.display.flip()

    with open('score.txt', 'w') as score_file:
        json.dump(score, score_file)

    pygame.quit()


if __name__ == '__main__':
    try:
        main()
        sys.exit()
    except:
        print('Sorry, something went wrong!')
        terminate()
