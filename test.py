import random
import pygame
from image_controller import load_image
import json
import time


class Crushing:

    def update_text(self):
        self.text1 = self.font.render('iron', True, (255, 255, 255))
        self.text2 = self.font.render('iron nuggets', True, (255, 255, 255))
        self.text3 = self.font.render(f'{self.score["iron"]}', True, (255, 255, 255))
        self.text4 = self.font.render(f'{self.score["iron nuggets"]}', True, (255, 255, 255))
        self.text5 = self.font.render('gold', True, (255, 255, 255))
        self.text6 = self.font.render('gold nuggets', True, (255, 255, 255))
        self.text7 = self.font.render(f'{self.score["gold"]}', True, (255, 255, 255))
        self.text8 = self.font.render(f'{self.score["gold nuggets"]}', True, (255, 255, 255))
        self.text9 = self.font.render("You don't have enough iron", True, (255, 255, 255))
        self.text10 = self.font.render("You don't have enough gold", True, (255, 255, 255))

    def __init__(self, screen, screen_size, score):

        self.score = score
        self.screen = screen
        self.screen_size = screen_size

        self.current = None
        self.start_sprites = pygame.sprite.Group()
        self.end_1_sprites = pygame.sprite.Group()
        self.end_2_sprites = pygame.sprite.Group()
        self.first_fill = False
        self.clicks = 0

        self.font = pygame.font.Font(None, 72)

        self.update_text()

        iron_ingots_image = load_image('iron_ingots.png', -1)
        iron_ingots = pygame.sprite.Sprite(self.start_sprites)
        iron_ingots_image = pygame.transform.scale(iron_ingots_image, (280, 200))
        self.iron_id = id(iron_ingots)
        iron_ingots.image = iron_ingots_image
        iron_ingots.rect = iron_ingots.image.get_rect()
        iron_ingots.rect.x = 150
        iron_ingots.rect.y = 400

        gold_ingots_image = load_image('gold_ingots.png', -1)
        gold_ingots = pygame.sprite.Sprite(self.start_sprites)
        gold_ingots_image = pygame.transform.scale(gold_ingots_image, (280, 200))
        self.gold_id = id(gold_ingots)
        gold_ingots.image = gold_ingots_image
        gold_ingots.rect = gold_ingots.image.get_rect()
        gold_ingots.rect.x = 570
        gold_ingots.rect.y = 400

        metal_sheet_image = load_image('metal_sheet.png', -1)
        metal_sheet = pygame.sprite.Sprite(self.end_1_sprites, self.end_2_sprites)
        metal_sheet_image = pygame.transform.scale(metal_sheet_image, (200, 200))
        metal_sheet.image = metal_sheet_image
        metal_sheet.rect = metal_sheet.image.get_rect()
        metal_sheet.rect.x = 400
        metal_sheet.rect.y = 400

        iron_image = load_image('iron.png', -1)
        iron = pygame.sprite.Sprite(self.end_1_sprites)
        iron_image = pygame.transform.scale(iron_image, (200, 200))
        iron.image = iron_image
        iron.rect = iron.image.get_rect()
        iron.rect.x = 400
        iron.rect.y = 400

        gold_image = load_image('gold.png', -1)
        gold = pygame.sprite.Sprite(self.end_2_sprites)
        gold_image = pygame.transform.scale(gold_image, (200, 200))
        gold.image = gold_image
        gold.rect = gold.image.get_rect()
        gold.rect.x = 400
        gold.rect.y = 400

        crush_image = load_image('crush.png', -1)
        crush = pygame.sprite.Sprite(self.end_1_sprites, self.end_2_sprites)
        crush_image = pygame.transform.scale(crush_image, (250, 250))
        crush.image = crush_image
        crush.rect = crush.image.get_rect()
        crush.rect.x = 360
        crush.rect.y = 80

    def get_event(self, image, event):
        if image.rect.collidepoint(event.pos):
            if id(image) == self.iron_id:
                if self.score['iron'] != 0:
                    self.current = 1
                else:
                    self.screen.blit(self.text9, (200, 100))

                    time.sleep(1)
                    self.screen.fill((0, 0, 0))
                    self.start_sprites.draw(self.screen)


            if id(image) == self.gold_id:
                if self.score['gold'] != 0:
                    self.current = 2
                else:
                    self.screen.blit(self.text10, (200, 100))

                    time.sleep(1)
                    self.screen.fill((0, 0, 0))
                    self.start_sprites.draw(self.screen)


    def main_crushing(self):
        self.start_sprites.draw(self.screen)

        if self.current == None:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        # mode = 1
                if event.type == pygame.MOUSEBUTTONUP:
                    for image in self.start_sprites:
                        self.get_event(image, event)

        elif self.current == 1:
            if not self.first_fill:
                self.screen.fill((0, 0, 0))
                self.end_1_sprites.draw(self.screen)
                self.first_fill = True
                self.screen.blit(self.text1, (50, 800))
                self.screen.blit(self.text2, (650, 800))
                self.screen.blit(self.text3, (50, 870))
                self.screen.blit(self.text4, (650, 870))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.current = None
                        self.screen.fill((0, 0, 0))
                        self.start_sprites.draw(self.screen)
                        self.first_fill = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.score['iron'] != 0:
                        self.clicks += 1
                        if self.clicks == 3:
                            self.score['iron'] -= 1
                            self.score['iron nuggets'] += random.randint(1, 3)
                            self.clicks = 0
                            self.screen.fill((0, 0, 0))
                            self.end_1_sprites.draw(self.screen)
                            self.update_text()
                            self.screen.blit(self.text1, (50, 800))
                            self.screen.blit(self.text2, (650, 800))
                            self.screen.blit(self.text3, (50, 870))
                            self.screen.blit(self.text4, (650, 870))
                    else:
                        self.current = None
                        self.screen.fill((0, 0, 0))
                        self.start_sprites.draw(self.screen)
                        self.first_fill = False

        elif self.current == 2:
            if not self.first_fill:
                self.screen.fill((0, 0, 0))
                self.end_2_sprites.draw(self.screen)
                self.screen.blit(self.text5, (50, 800))
                self.screen.blit(self.text6, (650, 800))
                self.screen.blit(self.text7, (50, 870))
                self.screen.blit(self.text8, (650, 870))

                self.first_fill = True
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.current = None
                        self.screen.fill((0, 0, 0))
                        self.start_sprites.draw(self.screen)

                        self.first_fill = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.score['gold'] != 0:
                        self.clicks += 1
                        if self.clicks == 3:
                            self.score['gold'] -= 1
                            self.score['gold nuggets'] += random.randint(1, 2)
                            self.clicks = 0
                            self.screen.fill((0, 0, 0))
                            self.end_2_sprites.draw(self.screen)
                            self.update_text()
                            self.screen.blit(self.text5, (50, 800))
                            self.screen.blit(self.text6, (650, 800))
                            self.screen.blit(self.text7, (50, 870))
                            self.screen.blit(self.text8, (650, 870))

                    else:
                        self.current = None
                        self.screen.fill((0, 0, 0))
                        self.start_sprites.draw(self.screen)

                        self.first_fill = False
