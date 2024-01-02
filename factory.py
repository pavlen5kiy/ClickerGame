import pygame
from image_loader import load_image
import time
import random


class Factory():
    def __init__(self):
        pygame.init()
        screen_info = pygame.display.Info()
        width, height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((width, height))
        all_sprites = pygame.sprite.Group()

        coal = 0
        iron = 0
        crushed_coal = 0
        crushed_iron = 0
        melted_iron = 0
        formed_iron = 0

        crushing_coal_time = 7
        crushing_iron_time = 9
        melting_time = 10
        forming_time = 10

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

        start_button_image = load_image('кнопка начала процесса.png', -1)
        start_button_image = pygame.transform.scale(start_button_image, (150, 40))
        start_button = pygame.sprite.Sprite(all_sprites)
        start_button.image = start_button_image
        start_button.rect = start_button.image.get_rect()
        start_button.rect.x = screen_info.current_w - 1550
        start_button.rect.y = screen_info.current_h - 440

        start_button = pygame.sprite.Sprite(all_sprites)
        start_button.image = start_button_image
        start_button.rect = start_button.image.get_rect()
        start_button.rect.x = screen_info.current_w - 1000
        start_button.rect.y = screen_info.current_h - 440

        start_button = pygame.sprite.Sprite(all_sprites)
        start_button.image = start_button_image
        start_button.rect = start_button.image.get_rect()
        start_button.rect.x = screen_info.current_w - 525
        start_button.rect.y = screen_info.current_h - 440

        update_button_image = load_image('кнопка улучшения.webp', -1)
        update_button_image = pygame.transform.scale(update_button_image, (150, 40))
        update_button = pygame.sprite.Sprite(all_sprites)
        update_button.image = update_button_image
        update_button.rect = update_button.image.get_rect()
        update_button.rect.x = screen_info.current_w - 1350
        update_button.rect.y = screen_info.current_h - 440

        update_button = pygame.sprite.Sprite(all_sprites)
        update_button.image = update_button_image
        update_button.rect = update_button.image.get_rect()
        update_button.rect.x = screen_info.current_w - 800
        update_button.rect.y = screen_info.current_h - 440

        update_button = pygame.sprite.Sprite(all_sprites)
        update_button.image = update_button_image
        update_button.rect = update_button.image.get_rect()
        update_button.rect.x = screen_info.current_w - 325
        update_button.rect.y = screen_info.current_h - 440


        all_sprites.draw(screen)
        pygame.display.flip()
        self.main()

    def crushing(self, coal, iron, crushed_coal, crushed_iron, crushing_coal_time, crushing_iron_time):
        while coal != 0:
            time.sleep(crushing_coal_time)
            coal -= 1
            crushed_coal += random.randint(2, 4)
        while iron != 0:
            time.sleep(crushing_iron_time)
            iron -= 1
            crushed_iron += random.randint(1, 3)

        return coal, iron, crushed_coal, crushed_iron

    def melting(self, crushed_coal, crushed_iron, melted_iron, melting_time):
        while crushed_iron > 1 and crushed_coal != 0:
            crushed_coal -= random.randint(1, 3)
            time.sleep(melting_time)
            if crushed_iron == 1:
                crushed_iron - 1
            else:
                crushed_iron -= random.randint(1, 2)
            melted_iron += 1

        return crushed_coal, crushed_iron, melted_iron

    def forming(self, melted_iron, forming_time, formed_iron):
        while melted_iron >= 3:
            melted_iron -= 3
            time.sleep(forming_time)
            formed_iron += 1

        return melted_iron, formed_iron

    def main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pass


if __name__ == '__main__':
    Factory()
