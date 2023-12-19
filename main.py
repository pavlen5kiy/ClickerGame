import pygame
from board import Board
from image_controller import load_image
from ui import Text, Table
from sprite_controller import Cursor


def log(output):
    print(f'LOG: ', output)


def background(screen):
    bg = load_image('background.jpeg')
    bg = pygame.transform.smoothscale(bg, screen.get_size())
    screen.blit(bg, (0, 0))


def screen_init():
    # Setting a game window with computer's screen size
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h
    log(f'screen resolution {(width, height)}')
    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption('Board dev')

    return screen, width, height


def make_board(size, screen_size):
    width, height = screen_size
    board = Board(*size, count=5)
    cell_size = 120
    left = width // 2 - board.width * cell_size // 2
    top = height // 2 - board.height * cell_size // 2
    board.set_view(left, top, cell_size)

    return board


def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Initializing screen
    screen, width, height = screen_init()

    # Making a board
    board = make_board((7, 7), (width, height))

    # Sprites
    cursor_group = pygame.sprite.Group()
    cursor_image = load_image("cursor.png")
    cursor = Cursor(cursor_image, cursor_group)

    # Resources table
    table = Table(screen, (width, height))

    # Game cycle
    running = True

    while running:
        clock.tick(120)

        render_cursor = False
        x, y = pygame.mouse.get_pos()
        mouse_in_area = board.left <= x <= board.left + board.width * board.cell_size and board.top <= y <= board.top + board.height * board.cell_size

        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(True)

            if mouse_in_area:
                pygame.mouse.set_visible(False)
                render_cursor = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.count and mouse_in_area:
                    board.get_click(event.pos, table)

        # Background
        background(screen)

        # Working with text
        text = Text(screen, (width, height))
        text.dig_count(board.count)

        if not board.count:
            text.game_over(board)
            table.render(screen)

        board.render(screen)

        # Cursor render
        if render_cursor:
            cursor_group.draw(screen)
        cursor.update()

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
