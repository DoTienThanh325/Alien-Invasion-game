import pygame
from pygame.sprite import Sprite 

class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load ảnh alien lên và lấy rect của ảnh
        self.image = pygame.image.load("D:/pythonLabICN/Alien Invasion remake/images/quaiVat.png")
        self.rect = self.image.get_rect()

        # set cho alien nằm ở top left cách lề trái = một alien và cách top bằng một alien 
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # lưu vị trí alien dưới dạng số float
        self.x = float(self.rect.x)
    
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.x <= 0:
            return True

    def update(self):
        self.x += (self.settings.alien_speed* self.settings.fleet_direction)
        self.rect.x = self.x 