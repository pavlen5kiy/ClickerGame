import pygame
from image_controller import load_image


class Crushing:
    def __init__(self):
        pygame.init()
        size = 1000, 1000
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((0, 0, 0))
        self.current = None
        self.start_sprites = pygame.sprite.Group()
        self.end_1_sprites = pygame.sprite.Group()
        self.end_2_sprites = pygame.sprite.Group()
        self.first_fill = False

        f1 = pygame.font.Font(None, 72)
        self.text1 = f1.render('iron', True, (255, 255, 255))

        f2 = pygame.font.Font(None, 72)
        self.text2 = f2.render('iron nuggets', True, (255, 255, 255))

        f3 = pygame.font.Font(None, 72)
        self.text3 = f3.render('0', True, (255, 255, 255))

        f4 = pygame.font.Font(None, 72)
        self.text4 = f4.render('0', True, (255, 255, 255))

        f5 = pygame.font.Font(None, 72)
        self.text5 = f5.render('gold', True, (255, 255, 255))

        f6 = pygame.font.Font(None, 72)
        self.text6 = f6.render('gold nuggets', True, (255, 255, 255))

        f7 = pygame.font.Font(None, 72)
        self.text7 = f7.render('0', True, (255, 255, 255))

        f8 = pygame.font.Font(None, 72)
        self.text8 = f8.render('0', True, (255, 255, 255))


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

        self.start_sprites.draw(self.screen)
        pygame.display.flip()
        self.running = True
        self.main_crushing()

    def get_event(self, image, event):
        if image.rect.collidepoint(event.pos):
            if id(image) == self.iron_id:
                self.current = 1
            elif id(image) == self.gold_id:
                self.current = 2

    def main_crushing(self):
        while self.running:
            if self.current == None:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
                            #mode = 1
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
                    if event.type == pygame.MOUSEBUTTONUP:
                        if


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

        pygame.quit()


if __name__ == '__main__':
    Crushing()
