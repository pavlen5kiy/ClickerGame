import pygame
from image_loader import load_image

class Factory():
    def __init__(self):
        pygame.init()
        screen_info = pygame.display.Info()
        width, height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((width, height))
        all_sprites = pygame.sprite.Group()

        factory_image = load_image('фабрика 2.webp')
        factory_image = pygame.transform.scale(factory_image, (screen_info.current_w, screen_info.current_h))

        factory = pygame.sprite.Sprite(all_sprites)
        factory.image = factory_image
        factory.rect = factory.image.get_rect()
        factory.rect.x = 0
        factory.rect.y = 0

        foundry_image = load_image('плавильная печь.jpg', -1)
        foundry_image = pygame.transform.scale(foundry_image, (350, 350))

        foundry = pygame.sprite.Sprite(all_sprites)
        foundry.image = foundry_image
        foundry.rect = foundry.image.get_rect()
        foundry.rect.x = screen_info.current_w - 1500
        foundry.rect.y = screen_info.current_h - 350
        all_sprites.draw(screen)
        pygame.display.flip()
        while pygame.event.wait().type != pygame.QUIT:
            pass
        pygame.quit()


Factory()