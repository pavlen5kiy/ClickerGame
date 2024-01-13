import pygame
from image_controller import load_image
from main import main
import time
import random


class Workshop():
    def __init__(self):
        pygame.init()
        screen_info = pygame.display.Info()
        width, height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((width, height))
        self.all_sprites = pygame.sprite.Group()
        self.crusher = False
        self.number_of_clicks_already_made = 0

        self.coal = 1
        self.iron = 1
        self.crushed_coal = 0
        self.crushed_iron = 0
        self.melted_iron = 0
        self.formed_iron = 0

        self.crushing_coal_number_of_clicks = 3
        self.crushing_iron_number_of_clicks = 4
        self.melting_time = 7
        self.forming_time = 8

        factory_image = load_image('фабрика 2.webp')
        factory_image = pygame.transform.scale(factory_image, (screen_info.current_w, screen_info.current_h))
        factory = pygame.sprite.Sprite(self.all_sprites)
        factory.image = factory_image
        factory.rect = factory.image.get_rect()
        factory.rect.x = 0
        factory.rect.y = 0

        foundry_image = load_image('плавильная печь.jpg', -1)
        foundry_image = pygame.transform.scale(foundry_image, (350, 350))
        foundry = pygame.sprite.Sprite(self.all_sprites)
        self.foundry_id = id(foundry)
        foundry.image = foundry_image
        foundry.rect = foundry.image.get_rect()
        foundry.rect.x = screen_info.current_w - 1000
        foundry.rect.y = screen_info.current_h - 350

        crusher_image = load_image('мельница шарового помола.webp', -1)
        crusher_image = pygame.transform.scale(crusher_image, (500, 500))
        crusher = pygame.sprite.Sprite(self.all_sprites)
        self.crusher_id = id(crusher)
        crusher.image = crusher_image
        crusher.rect = crusher.image.get_rect()
        crusher.rect.x = screen_info.current_w - 1600
        crusher.rect.y = screen_info.current_h - 400

        molds_image = load_image('формочки для слитков.jpg', -1)
        molds_image = pygame.transform.scale(molds_image, (400, 400))
        molds = pygame.sprite.Sprite(self.all_sprites)
        self.molds_id = id(molds)
        molds.image = molds_image
        molds.rect = molds.image.get_rect()
        molds.rect.x = screen_info.current_w - 550
        molds.rect.y = screen_info.current_h - 400

        chest_image = load_image('chest.png', -1)
        chest_image = pygame.transform.scale(chest_image, (200, 200))
        chest = pygame.sprite.Sprite(self.all_sprites)
        self.chest_id = id(chest)
        chest.image = chest_image
        chest.rect = chest.image.get_rect()
        chest.rect.x = screen_info.current_w - 220
        chest.rect.y = 40

        map_image = load_image('map.png', -1)
        map_image = pygame.transform.scale(map_image, (200, 200))
        map = pygame.sprite.Sprite(self.all_sprites)
        self.map_id = id(map)
        map.image = map_image
        map.rect = map.image.get_rect()
        map.rect.x = 40
        map.rect.y = 40

        self.all_sprites.draw(screen)
        pygame.display.flip()
        self.ws_main()

    def crushing(self):
        self.crusher = True

    def melting(self):
        while self.crushed_iron > 1 and self.crushed_coal != 0:
            self.crushed_coal -= random.randint(1, 3)
            time.sleep(self.melting_time)
            if self.crushed_iron == 1:
                self.crushed_iron -= 1
            else:
                self.crushed_iron -= random.randint(1, 2)
            self.melted_iron += 1
        if self.crushed_coal < 0:
            self.crushed_coal = 0

        return self.crushed_coal, self.crushed_iron, self.melted_iron

    def forming(self):
        while self.melted_iron >= 3:
            self.melted_iron -= 3
            time.sleep(self.forming_time)
            self.formed_iron += 1

        return self.melted_iron, self.formed_iron

    def get_event(self, image, event):
        if image.rect.collidepoint(event.pos):
            if id(image) == self.map_id:
                main()
            elif id(image) == self.molds_id:
                self.forming()
            elif id(image) == self.foundry_id:
                self.melting()
            elif id(image) == self.crusher_id:
                self.crushing()
                print(self.coal, self.iron, self.crushed_iron, self.crushed_coal)
            elif id(image) == self.chest_id:
                pass

    def ws_main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP and not self.crusher:
                    for image in self.all_sprites:
                        self.get_event(image, event)
                if event.type == pygame.MOUSEBUTTONUP and self.crusher:
                    self.number_of_clicks_already_made += 1
                    if self.number_of_clicks_already_made == self.crushing_coal_number_of_clicks and self.coal != 0:
                        self.coal -= 1
                        self.crushed_coal += random.randint(1, 4)
                        self.number_of_clicks_already_made = 0
                    elif self.number_of_clicks_already_made == self.crushing_iron_number_of_clicks and self.iron != 0:
                        self.iron -= 1
                        self.crushed_iron += random.randint(1, 3)
                    elif self.coal == 0 and self.iron == 0:
                        self.crusher = False


if __name__ == '__main__':
    Workshop()