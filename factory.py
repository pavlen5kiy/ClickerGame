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
        foundry.rect.x = screen_info.current_w - 1000
        foundry.rect.y = screen_info.current_h - 350

        crusher_image = load_image('мельница шарового помола.webp', -1)
        crusher_image = pygame.transform.scale(crusher_image, (500, 500))
        crusher = pygame.sprite.Sprite(all_sprites)
        crusher.image = crusher_image
        crusher.rect = crusher.image.get_rect()
        crusher.rect.x = screen_info.current_w - 1600
        crusher.rect.y = screen_info.current_h - 400

        molds_image = load_image('формочки для слитков.jpg', -1)
        molds_image = pygame.transform.scale(molds_image, (400, 400))
        molds = pygame.sprite.Sprite(all_sprites)
        molds.image = molds_image
        molds.rect = molds.image.get_rect()
        molds.rect.x = screen_info.current_w - 550
        molds.rect.y = screen_info.current_h - 400

        chest_image = load_image('сундук.webp', -1)
        chest_image = pygame.transform.scale(chest_image, (200, 200))
        chest = pygame.sprite.Sprite(all_sprites)
        chest.image = chest_image
        chest.rect = chest.image.get_rect()
        chest.rect.x = screen_info.current_w - 220
        chest.rect.y = 40

        map_image = load_image('карта.webp', -1)
        map_image = pygame.transform.scale(map_image, (200, 200))
        map = pygame.sprite.Sprite(all_sprites)
        map.image = map_image
        map.rect = map.image.get_rect()
        map.rect.x = 40
        map.rect.y = 40

        all_sprites.draw(screen)
        pygame.display.flip()
        while pygame.event.wait().type != pygame.QUIT:
            pass
        pygame.quit()


Factory()