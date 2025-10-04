import pygame.font
from pygame.sprite import Group
from heart import Heart
class Scoreboard:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Thiết lập font cho điểm số
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Chuẩn bị hình ảnh điểm số ban đầu
        self.prep_score()
        
        # Set điểm số cao nhất
        self.prep_high_score()

        # Chuẩn bị hình ảnh level
        self.prep_level()

        # Chuẩn bị hình ảnh số mạng còn lại
        self.prep_hearts()
    
    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, None)

        # Hiển thị điểm số ở góc trên bên phải
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20 
        self.score_rect.top = 20
    
    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, None)

        # Hiển thị điểm số ở giữa trên cùng
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    
    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, None)

        # Hiển thị level dưới điểm số
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    
    def prep_hearts(self):
        self.hearts = Group()
        for heart_number in range(self.stats.ship_left):
            heart = Heart(self.ai_game)
            heart.rect.x = 10 + heart_number * (heart.rect.width + 10)
            heart.rect.y = 10
            self.hearts.add(heart)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.hearts.draw(self.screen)