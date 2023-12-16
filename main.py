import pygame
from board import Board
from image_loader import load_image
from resources_table import Table


def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Setting a game window with computer's screen size
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h
    # width, height = 1920, 1080
    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption('Board dev')

    # Making a board
    board = Board(7, 7)
    cell_size = 120
    left = width // 2 - board.width * cell_size // 2
    top = height // 2 - board.height * cell_size // 2
    board.set_view(left, top, cell_size)

    # Sprites
    all_sprites = pygame.sprite.Group()

    cursor_image = load_image("cursor.png")
    cursor = pygame.sprite.Sprite(all_sprites)
    cursor.image = cursor_image
    cursor.rect = cursor.image.get_rect()

    # Resources table
    table = Table()

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

                cursor.rect.topleft = pygame.mouse.get_pos()
                render_cursor = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.count and mouse_in_area:
                    board.get_click(event.pos, table)

        # screen.fill('#f4a460')
        background = load_image('mango-y-banana-2.jpg')
        background = pygame.transform.smoothscale(background,
                                                  screen.get_size())
        screen.blit(background, (0, 0))

        # Working with text
        font = pygame.font.Font(None, 100)
        if board.count:
            board.count_label = font.render(str(board.count), True, 'white')
        else:
            board.count_label = font.render(str(board.count), True, 'red')
        screen.blit(board.count_label, (20, 20))

        if not board.count:
            text = font.render("Game Over!", True, 'white')
            screen.blit(text, (width // 2 - text.get_width() // 2, board.top + board.cell_size * board.height + 50))
            table.render(screen)

        board.render(screen)

        # Cursor render
        if render_cursor:
            all_sprites.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
