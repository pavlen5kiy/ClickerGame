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
        self.gold = 0
        self.iron_nuggets = 0
        self.gold_nuggets = 0
        self.melt_iron = 0
        self.melt_gold = 0
        self.gold_ingots = 0
        self.iron_ingots = 0

        self.crushing_gold_number_of_clicks = 3
        self.crushing_iron_number_of_clicks = 4
        self.melting_iron_time = 7
        self.melting_gold_time = 6
        self.forming_time = 8
        self.number_of_molds = 2

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
        while self.iron_nuggets > 0 and self.coal > 0:
            self.coal -= random.randint(1, 3)
            time.sleep(self.melting_iron_time)
            if self.iron_nuggets == 1:
                self.iron_nuggets -= 1
            else:
                self.iron_nuggets -= random.randint(1, 2)
            self.melt_iron += 1
        if self.coal < 0:
            self.coal = 0

        while self.gold_nuggets > 1 and self.coal > 0:
            self.coal -= random.randint(1, 3)
            time.sleep(self.melting_gold_time)
            if self.gold_nuggets == 2:
                self.gold_nuggets -= 2
            else:
                self.gold_nuggets -= random.randint(2, 3)
            self.melt_gold += 1
        if self.coal < 0:
            self.coal = 0

        return self.coal, self.iron_nuggets, self.gold_nuggets, self.melt_iron, self.melt_gold

    def forming(self):
        while self.melt_iron >= 3 * self.number_of_molds:
            self.melt_iron -= 3 * self.number_of_molds
            time.sleep(self.forming_time)
            self.iron_ingots += self.number_of_molds

        while self.melt_gold >= 3 * self.number_of_molds:
            self.melt_gold -= 3 * self.number_of_molds
            time.sleep(self.forming_time)
            self.gold_ingots += self.number_of_molds

        return self.melt_iron, self.melt_gold, self.iron_ingots, self.gold_ingots

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
                    if self.number_of_clicks_already_made == self.crushing_gold_number_of_clicks and self.gold != 0:
                        self.gold -= 1
                        self.gold_nuggets += random.randint(1, 3)
                        self.number_of_clicks_already_made = 0
                    elif self.number_of_clicks_already_made == self.crushing_iron_number_of_clicks and self.iron != 0:
                        self.iron -= 1
                        self.iron_nuggets += random.randint(1, 4)
                    elif self.gold == 0 and self.iron == 0:
                        self.crusher = False


if __name__ == '__main__':
    Workshop()
