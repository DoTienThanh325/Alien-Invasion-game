import pygame 
from pygame.sprite import Sprite
class Heart(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load ảnh heart và lấy rect của ảnh
        self.image = pygame.image.load("D:/pythonLabICN/Alien Invasion remake/images/heart.png")
        self.rect = self.image.get_rect()
        self.screen_rect = ai_game.screen.get_rect()
        self.rect.x = 10
        self.rect.y = 10
        self.x = float(self.rect.x)
    
    