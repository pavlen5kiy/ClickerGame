import pygame
from board import Board
from image_loader import load_image


def main():
    pygame.init()

    # Setting a game window with computer's screen size
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption('Board dev')

    # Making a board
    board = Board(7, 7)
    cell_size = 120
    left = width // 2 - board.width * cell_size // 2
    top = height // 2 - board.height * cell_size // 2
    board.set_view(left, top, cell_size)

    # Making a dig count
    count = 5

    # Sprites
    all_sprites = pygame.sprite.Group()

    cursor_image = load_image("cursor.png")
    cursor = pygame.sprite.Sprite(all_sprites)
    cursor.image = cursor_image
    cursor.rect = cursor.image.get_rect()

    pygame.mouse.set_visible(False)

    # Game cycle
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION:
                cursor.rect.topleft = event.pos

            if event.type == pygame.MOUSEBUTTONDOWN:
                if count:
                    board.get_click(event.pos)
                    count -= 1

        screen.fill('#f4a460')

        # Working with text
        font = pygame.font.Font(None, 100)
        if count:
            count_label = font.render(str(count), True, 'white')
        else:
            count_label = font.render(str(count), True, 'red')
        screen.blit(count_label, (20, 20))

        if not count:
            text = font.render("Game Over!", True, 'white')
            screen.blit(text, (width // 2 - text.get_width() // 2, 1100))

        board.render(screen)

        # Cursor render
        if pygame.mouse.get_focused():
            all_sprites.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
