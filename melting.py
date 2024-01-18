import random
import pygame
from image_controller import load_image
import json
import time

class Melting:
    def update_text(self):
        self.text1 = self.f1.render('iron nuggets', True, (255, 255, 255))
        self.text2 = self.f2.render('melt iron', True, (255, 255, 255))
        self.text3 = self.f3.render(f'{self.score["iron nuggets"]}', True, (255, 255, 255))
        self.text4 = self.f4.render(f'{self.score["melt iron"]}', True, (255, 255, 255))
        self.text5 = self.f5.render('gold nuggets', True, (255, 255, 255))
        self.text6 = self.f6.render('melt gold', True, (255, 255, 255))
        self.text7 = self.f7.render(f'{self.score["gold nuggets"]}', True, (255, 255, 255))
        self.text8 = self.f8.render(f'{self.score["melt gold"]}', True, (255, 255, 255))
        self.text9 = self.f9.render("You don't have enough iron nuggets", True, (255, 255, 255))
        self.text10 = self.f10.render("You don't have enough gold nuggets", True, (255, 255, 255))
        self.text11 = self.f11.render(f"{self.time_left}", True, (255, 255, 255))

    def __init__(self):
        try:
            with open('score.txt') as score_file:
                self.score = json.load(score_file)
        except:
            print('No file created yet')

        self.score = {
            'coins': 9999,
            'gems': 9999,
            'coal': 1000,
            'iron': 100,
            'gold': 100,
            'iron nuggets': 100,
            'gold nuggets': 100,
            'melt iron': 0,
            'melt gold': 0,
            'iron ingots': 0,
            'gold ingots': 0,
            'digging': [5, [5, 10, 20, 35, 49], [0, 200, 600, 1000, 1500], 'clk'],
            'crushing': [10, [10, 7, 5, 3], [0, 200, 600, 1000], 'clk'],
            'melting time': [10, [10, 7, 5, 3], [0, 500, 1000, 2000], 'sec'],
            'exchange gems': [20, [20, 15, 10], [0, 10000, 20000], 'gem']}

        pygame.init()
        size = 1000, 1000
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((0, 0, 0))
        self.current = None
        self.start_sprites = pygame.sprite.Group()
        self.end_1_sprites = pygame.sprite.Group()
        self.end_2_sprites = pygame.sprite.Group()
        self.first_fill = False
        self.time_left = 0

        self.f1 = pygame.font.Font(None, 72)
        self.f2 = pygame.font.Font(None, 72)
        self.f3 = pygame.font.Font(None, 72)
        self.f4 = pygame.font.Font(None, 72)
        self.f5 = pygame.font.Font(None, 72)
        self.f6 = pygame.font.Font(None, 72)
        self.f7 = pygame.font.Font(None, 72)
        self.f8 = pygame.font.Font(None, 72)
        self.f9 = pygame.font.Font(None, 72)
        self.f10 = pygame.font.Font(None, 72)
        self.f11 = pygame.font.Font(None, 72)

        self.update_text()

        iron_ingots_image = load_image('iron_ingots.png', -1)
        iron_ingots = pygame.sprite.Sprite(self.start_sprites)
        iron_ingots_image = pygame.transform.scale(iron_ingots_image, (280, 200))
        self.iron_id = id(iron_ingots)
        iron_ingots.image = iron_ingots_image
        iron_ingots.rect = iron_ingots.image.get_rect()
        iron_ingots.rect.x = 150
        iron_ingots.rect.y = 400

        # iron_image_highlighted = load_image('iron_ingots_highlited.png', -1)
        # iron_highlighted = pygame.sprite.Sprite()
        # iron_image_highlighted = pygame.transform.scale(iron_image_highlighted, (280, 200))
        # self.iron_highlighted_id = id(iron_highlighted)
        # iron_highlighted.image = iron_image_highlighted
        # iron_highlighted.rect = iron_highlighted.image.get_rect()
        # iron_highlighted.rect.x = 150
        # iron_highlighted.rect.y = 200

        gold_ingots_image = load_image('gold_ingots.png', -1)
        gold_ingots = pygame.sprite.Sprite(self.start_sprites)
        gold_ingots_image = pygame.transform.scale(gold_ingots_image, (280, 200))
        self.gold_id = id(gold_ingots)
        gold_ingots.image = gold_ingots_image
        gold_ingots.rect = gold_ingots.image.get_rect()
        gold_ingots.rect.x = 570
        gold_ingots.rect.y = 400

        # gold_image_highlighted = load_image('gold_ingots_highlited.png', -1)
        # gold_highlighted = pygame.sprite.Sprite()
        # gold_image_highlighted = pygame.transform.scale(gold_image_highlighted, (280, 200))
        # self.gold_highlighted_id = id(gold_highlighted)
        # gold_highlighted.image = gold_image_highlighted
        # gold_highlighted.rect = gold_highlighted.image.get_rect()
        # gold_highlighted.rect.x = 570
        # gold_highlighted.rect.y = 200

        melt_image = load_image('bucket.png', -1)
        melt = pygame.sprite.Sprite(self.end_1_sprites, self.end_2_sprites)
        melt_image = pygame.transform.scale(melt_image, (250, 250))
        melt.image = melt_image
        melt.rect = melt.image.get_rect()
        melt.rect.x = 360
        melt.rect.y = 80

        self.start_sprites.draw(self.screen)
        pygame.display.flip()
        self.running = True
        self.main_crushing()

    def get_event(self, image, event):
        if image.rect.collidepoint(event.pos):
            if id(image) == self.iron_id:
                if self.score['iron nuggets'] != 0:
                    self.current = 1
                else:
                    self.screen.blit(self.text9, (85, 100))
                    pygame.display.flip()
                    time.sleep(0.75)
                    self.screen.fill((0, 0, 0))
                    self.start_sprites.draw(self.screen)
                    pygame.display.flip()

            if id(image) == self.gold_id:
                if self.score['gold nuggets'] != 0:
                    self.current = 2
                else:
                    self.screen.blit(self.text10, (85, 100))
                    pygame.display.flip()
                    time.sleep(0.75)
                    self.screen.fill((0, 0, 0))
                    self.start_sprites.draw(self.screen)
                    pygame.display.flip()

    def main_crushing(self):
        while self.running:
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
                    pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.current = None
                            self.screen.fill((0, 0, 0))
                            self.start_sprites.draw(self.screen)
                            pygame.display.flip()
                            self.first_fill = False
                    if self.score['iron nuggets'] != 0:
                        if self.time_left != 0:
                            for _ in range(4):
                                time.sleep(1)
                                self.time_left -= 1
                                self.update_text()
                            self.score['iron nuggets'] -= 3
                            self.score['melt iron'] += 1
                            self.clicks = 0
                            self.screen.fill((0, 0, 0))
                            self.end_1_sprites.draw(self.screen)
                            self.update_text()
                            self.screen.blit(self.text1, (50, 800))
                            self.screen.blit(self.text2, (650, 800))
                            self.screen.blit(self.text3, (50, 870))
                            self.screen.blit(self.text4, (650, 870))
                            pygame.display.flip()
                    else:
                        self.current = None
                        self.screen.fill((0, 0, 0))
                        self.start_sprites.draw(self.screen)
                        pygame.display.flip()
                        self.first_fill = False

            elif self.current == 2:
                if not self.first_fill:
                    self.screen.fill((0, 0, 0))
                    self.end_2_sprites.draw(self.screen)
                    self.screen.blit(self.text5, (50, 800))
                    self.screen.blit(self.text6, (650, 800))
                    self.screen.blit(self.text7, (50, 870))
                    self.screen.blit(self.text8, (650, 870))
                    pygame.display.flip()
                    self.first_fill = True
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.current = None
                            self.screen.fill((0, 0, 0))
                            self.start_sprites.draw(self.screen)
                            pygame.display.flip()
                            self.first_fill = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        if self.score['gold nuggets'] != 0:
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
                                pygame.display.flip()
                        else:
                            self.current = None
                            self.screen.fill((0, 0, 0))
                            self.start_sprites.draw(self.screen)
                            pygame.display.flip()
                            self.first_fill = False

        pygame.quit()


if __name__ == '__main__':
    Melting()