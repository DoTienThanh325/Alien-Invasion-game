import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # xác định vị trí kích thước cho đạn
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Lưu trữ vị trí của đạn là số float
        self.y = float(self.rect.y)
    
    def update(self):
        # Cập nhật vị trí của đạn
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        # vẽ lại đạn
        pygame.draw.rect(self.screen, self.color, self.rect)