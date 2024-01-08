import pygame
from ui import Ui
from image_controller import load_image


class Money(Ui):
    def __init__(self, screen, screen_size):
        super().__init__(screen, screen_size)
        self.font = pygame.font.Font(None, 75)
        self.coins = 0
        self.gems = 0

    def render(self):
        coin = load_image('coin.png')
        gem = load_image('gem.png')
        offset = 10

        self.screen.blit(coin, (self.width - offset - coin.get_width(), 14))
        coins = self.font.render(str(self.coins), True, '#fdd179')
        self.screen.blit(coins,
                         (self.width - offset - 75 - coins.get_width(),
                          14 + (coin.get_height() - coins.get_height())))

        self.screen.blit(gem, (self.width - offset - gem.get_width(), 84))
        gems = self.font.render((str(self.gems)), True, '#cae6d9')
        self.screen.blit(gems,
                         (self.width - offset - 75 - gems.get_width(),
                          84 + (gem.get_height() - gems.get_height())))


class Resources:
    def __init__(self):
        self.resources = {
            'Coal': 0,
            'Iron': 0,
            'Gold': 0,
        }