import random
import pygame
from image_controller import load_image
import json
import time

class Casting:
    def update_text(self):
        self.text1 = self.f.render('melt iron', True, (255, 255, 255))
        self.text2 = self.f.render('iron ingots', True, (255, 255, 255))
        self.text3 = self.f.render(f'{self.score["melt iron"]}', True, (255, 255, 255))
        self.text4 = self.f.render(f'{self.score["iron ingots"]}', True, (255, 255, 255))
        self.text5 = self.f.render('melt gold', True, (255, 255, 255))
        self.text6 = self.f.render('gold ingots', True, (255, 255, 255))
        self.text7 = self.f.render(f'{self.score["melt gold"]}', True, (255, 255, 255))
        self.text8 = self.f.render(f'{self.score["gold ingots"]}', True, (255, 255, 255))
        self.text9 = self.f.render("You don't have enough melt iron", True, (255, 255, 255))
        self.text10 = self.f.render("You don't have enough melt gold", True, (255, 255, 255))
        self.text11 = self.f.render(f"wait: {self.time_left}", True, (255, 255, 255))
        self.text14 = self.f.render(f'You got {self.received_iron_ingots} iron ingots', True, (255, 255, 255))
        self.text15 = self.f.render(f'You got {self.received_gold_ingots} gold ingots', True, (255, 255, 255))

    def __init__(self):
        try:
            with open('score.txt') as score_file:
                self.score = json.load(score_file)
        except:
            print('No file created yet')

        self.score = {
            'coins': 9999,
            'gems': 9999,
            'coal': 4,
            'iron': 10,
            'gold': 10,
            'iron nuggets': 5,
            'gold nuggets': 100,
            'melt iron': 1,
            'melt gold': 10,
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
        self.received_iron_ingots = 0
        self.received_gold_ingots = 0
        self.number_of_molds = 3

        self.f = pygame.font.Font(None, 72)

        self.update_text()

        iron_ingots_image = load_image('iron_ingots.png', -1)
        iron_ingots = pygame.sprite.Sprite(self.start_sprites)
        iron_ingots_image = pygame.transform.scale(iron_ingots_image, (280, 200))
        self.iron_id = id(iron_ingots)
        iron_ingots.image = iron_ingots_image
        iron_ingots.rect = iron_ingots.image.get_rect()
        iron_ingots.rect.x = 150
        iron_ingots.rect.y = 400

        iron_ingots_image = load_image('iron_ingots.png', -1)
        iron_ingots = pygame.sprite.Sprite(self.end_1_sprites)
        iron_ingots_image = pygame.transform.scale(iron_ingots_image, (280, 200))
        iron_ingots.image = iron_ingots_image
        iron_ingots.rect = iron_ingots.image.get_rect()
        iron_ingots.rect.x = 360
        iron_ingots.rect.y = 300

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

        gold_ingots_image = load_image('gold_ingots.png', -1)
        gold_ingots = pygame.sprite.Sprite(self.end_2_sprites)
        gold_ingots_image = pygame.transform.scale(gold_ingots_image, (280, 200))
        gold_ingots.image = gold_ingots_image
        gold_ingots.rect = gold_ingots.image.get_rect()
        gold_ingots.rect.x = 360
        gold_ingots.rect.y = 300

        # gold_image_highlighted = load_image('gold_ingots_highlited.png', -1)
        # gold_highlighted = pygame.sprite.Sprite()
        # gold_image_highlighted = pygame.transform.scale(gold_image_highlighted, (280, 200))
        # self.gold_highlighted_id = id(gold_highlighted)
        # gold_highlighted.image = gold_image_highlighted
        # gold_highlighted.rect = gold_highlighted.image.get_rect()
        # gold_highlighted.rect.x = 570
        # gold_highlighted.rect.y = 200

        self.start_sprites.draw(self.screen)
        pygame.display.flip()
        self.running = True
        self.main_crushing()

    def get_event(self, image, event):
        if image.rect.collidepoint(event.pos):
            if id(image) == self.iron_id:
                if self.score['melt iron'] >= 3:
                    self.current = 1
                    self.time_left = 15 * (self.score['melt iron'] // (self.number_of_molds * 3))
                else:
                    self.screen.blit(self.text9, (90, 100))
                    pygame.display.flip()
                    time.sleep(0.75)
                    self.screen.fill((0, 0, 0))
                    self.start_sprites.draw(self.screen)
                    pygame.display.flip()

            if id(image) == self.gold_id:
                if self.score['melt gold'] >= 3:
                    self.current = 2
                    self.time_left = 18 * (self.score['melt gold'] // (self.number_of_molds * 3))
                else:
                    self.screen.blit(self.text10, (90, 100))
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
                    self.screen.blit(self.text11, (400, 800))
                    pygame.display.flip()

                while self.score['melt iron'] > 3:
                    if self.time_left != 0:
                        for _ in range(15):
                            time.sleep(1)
                            self.time_left -= 1
                            self.screen.fill((0, 0, 0))
                            self.update_text()
                            self.end_1_sprites.draw(self.screen)
                            self.screen.blit(self.text1, (50, 800))
                            self.screen.blit(self.text2, (650, 800))
                            self.screen.blit(self.text3, (50, 870))
                            self.screen.blit(self.text4, (650, 870))
                            self.screen.blit(self.text11, (400, 800))
                            pygame.display.flip()
                        if self.score['melt iron'] >= 3 * self.number_of_molds:
                            self.score['melt iron'] -= 3 * self.number_of_molds
                            self.score['iron ingots'] += self.number_of_molds
                            self.received_iron_ingots += self.number_of_molds
                        else:
                            molds_used = self.score['melt iron'] // 3
                            self.score['melt iron'] -= 3 * molds_used
                            self.score['iron ingots'] += molds_used
                            self.received_iron_ingots += molds_used
                        self.screen.fill((0, 0, 0))
                        self.update_text()
                        self.end_1_sprites.draw(self.screen)
                        self.screen.blit(self.text1, (50, 800))
                        self.screen.blit(self.text2, (650, 800))
                        self.screen.blit(self.text3, (50, 870))
                        self.screen.blit(self.text4, (650, 870))
                        self.screen.blit(self.text11, (400, 800))
                        pygame.display.flip()
                else:
                    self.current = None
                    self.screen.fill((0, 0, 0))
                    self.start_sprites.draw(self.screen)
                    self.screen.blit(self.text14, (300, 100))
                    pygame.display.flip()
                    time.sleep(1.25)
                    self.screen.fill((0, 0, 0))
                    self.start_sprites.draw(self.screen)
                    pygame.display.flip()
                    self.first_fill = False
                    self.received_iron_ingots = 0

            elif self.current == 2:
                if not self.first_fill:
                    self.screen.fill((0, 0, 0))
                    self.end_2_sprites.draw(self.screen)
                    self.screen.blit(self.text5, (50, 800))
                    self.screen.blit(self.text6, (650, 800))
                    self.screen.blit(self.text7, (50, 870))
                    self.screen.blit(self.text8, (650, 870))
                    self.screen.blit(self.text11, (400, 800))
                    pygame.display.flip()
                    self.first_fill = True

                while self.score['melt gold'] > 3:
                    if self.time_left != 0:
                        for _ in range(18):
                            time.sleep(1)
                            self.time_left -= 1
                            self.screen.fill((0, 0, 0))
                            self.update_text()
                            self.end_2_sprites.draw(self.screen)
                            self.screen.blit(self.text5, (50, 800))
                            self.screen.blit(self.text6, (650, 800))
                            self.screen.blit(self.text7, (50, 870))
                            self.screen.blit(self.text8, (650, 870))
                            self.screen.blit(self.text11, (400, 800))
                            pygame.display.flip()
                        if self.score['melt gold'] >= 3 * self.number_of_molds:
                            self.score['melt gold'] -= 3 * self.number_of_molds
                            self.score['gold ingots'] += self.number_of_molds
                            self.received_gold_ingots += self.number_of_molds
                        else:
                            molds_used = self.score['melt gold'] // 3
                            self.score['melt gold'] -= 3 * molds_used
                            self.score['gold ingots'] += molds_used
                            self.received_gold_ingots += molds_used
                        self.screen.fill((0, 0, 0))
                        self.update_text()
                        self.end_2_sprites.draw(self.screen)
                        self.screen.blit(self.text5, (50, 800))
                        self.screen.blit(self.text6, (650, 800))
                        self.screen.blit(self.text7, (50, 870))
                        self.screen.blit(self.text8, (650, 870))
                        self.screen.blit(self.text11, (400, 800))
                        pygame.display.flip()
                else:
                    self.current = None
                    self.screen.fill((0, 0, 0))
                    self.start_sprites.draw(self.screen)
                    self.screen.blit(self.text15, (300, 100))
                    pygame.display.flip()
                    time.sleep(1.25)
                    self.screen.fill((0, 0, 0))
                    self.start_sprites.draw(self.screen)
                    pygame.display.flip()
                    self.first_fill = False
                    self.received_gold_ingots = 0

        pygame.quit()


if __name__ == '__main__':
    Casting()
