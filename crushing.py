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
        self.end_sprites = pygame.sprite.Group()
        self.first_fill = False

        iron_image = load_image('iron_ingots.png', -1)
        iron = pygame.sprite.Sprite(self.start_sprites)
        iron_image = pygame.transform.scale(iron_image, (280, 200))
        self.iron_id = id(iron)
        iron.image = iron_image
        iron.rect = iron.image.get_rect()
        iron.rect.x = 150
        iron.rect.y = 200

        # iron_image_highlighted = load_image('iron_ingots_highlited.png', -1)
        # iron_highlighted = pygame.sprite.Sprite()
        # iron_image_highlighted = pygame.transform.scale(iron_image_highlighted, (280, 200))
        # self.iron_highlighted_id = id(iron_highlighted)
        # iron_highlighted.image = iron_image_highlighted
        # iron_highlighted.rect = iron_highlighted.image.get_rect()
        # iron_highlighted.rect.x = 150
        # iron_highlighted.rect.y = 200

        gold_image = load_image('gold_ingots.png', -1)
        gold = pygame.sprite.Sprite(self.start_sprites)
        gold_image = pygame.transform.scale(gold_image, (280, 200))
        self.gold_id = id(gold)
        gold.image = gold_image
        gold.rect = gold.image.get_rect()
        gold.rect.x = 570
        gold.rect.y = 200

        # gold_image_highlighted = load_image('gold_ingots_highlited.png', -1)
        # gold_highlighted = pygame.sprite.Sprite()
        # gold_image_highlighted = pygame.transform.scale(gold_image_highlighted, (280, 200))
        # self.gold_highlighted_id = id(gold_highlighted)
        # gold_highlighted.image = gold_image_highlighted
        # gold_highlighted.rect = gold_highlighted.image.get_rect()
        # gold_highlighted.rect.x = 570
        # gold_highlighted.rect.y = 200

        metal_sheet_image = load_image('metal_sheet.png', -1)
        metal_sheet = pygame.sprite.Sprite(self.end_sprites)
        metal_sheet_image = pygame.transform.scale(metal_sheet_image, (200, 200))
        metal_sheet.image = metal_sheet_image
        metal_sheet.rect = metal_sheet.image.get_rect()
        metal_sheet.rect.x = 400
        metal_sheet.rect.y = 400

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
                    self.end_sprites.draw(self.screen)
                    pygame.display.flip()
                    self.first_fill = True
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.current = None
                            self.start_sprites.draw(self.screen)
                            pygame.display.flip()
                            self.first_fill = False


            elif self.current == 2:
                if not self.first_fill:
                    self.screen.fill((0, 0, 0))
                    self.end_sprites.draw(self.screen)
                    pygame.display.flip()
                    self.first_fill = True
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.current = None
                            self.start_sprites.draw(self.screen)
                            pygame.display.flip()
                            self.first_fill = False

        pygame.quit()


if __name__ == '__main__':
    Crushing()
