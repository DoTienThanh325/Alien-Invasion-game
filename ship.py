import pygame

class Ship:
    def __init__(self, ai_game):
        # Lấy định dạng màn hình game
        self.screen = ai_game.screen 
        self.screen_rect = ai_game.screen.get_rect()

        # Lấy thông số settings ở file settings.py qua ai_game
        self.settings = ai_game.settings

        # Tạo biến image và lấy kích thước của ảnh
        self.image = pygame.image.load("Alien Invasion remake/images/spaceship.png")
        self.rect = self.image.get_rect()

        # Cho vị trí trung tâm cạnh dưới của ảnh trùng vời trung tâm cạnh dưới của màn hình
        self.rect.midbottom = self.screen_rect.midbottom

        # Biến kiểm tra xem tàu có dịch trái hay phải không
        self.moving_left = False
        self.moving_right = False 

        # lưu trữ vị trí con tàu là số thực 
        self.x = float(self.rect.x)
    
    def update(self):
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        # Cập nhật vị trí hoành độ con tàu
        self.rect.x = self.x 
    
    def blitme(self):
        # Vẽ hình ảnh với tọa độ và vị trí đã xác định
        self.screen.blit(self.image, self.rect)