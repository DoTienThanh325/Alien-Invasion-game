import pygame
from sys import exit
from settings import Settings
from ship import Ship 
from bullet import Bullet 
class AlienInvasion:
    def __init__(self):
        # Khởi tạo pygame
        pygame.init()
        
        # Khởi tạo biến setting để lấy các thuộc tính chung trong file settings.py
        self.settings = Settings()

        # Cài đặt kích thước và tên cho cửa sổ game

        # fullscreen
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_height = self.screen.get_rect().height
        # self.settings.screen_width = self.screen.get_rect().width

        # fixsize
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Khởi tạo con tàu
        self.ship = Ship(self)

        # lưu đạn vào một nhóm
        self.bullets = pygame.sprite.Group()

        # Cài đặt background
        self.bg_color = pygame.image.load('Alien Invasion remake/images/bg.jpg')
        self.bg_color = pygame.transform.scale(self.bg_color, (self.settings.screen_width, self.settings.screen_height))
    
    # Hàm chạy game
    def run_game(self):
        while True:
            # Check các sự kiện
            self._check_event()
            # update hoạt động của con tàu
            self.ship.update()
            # update đường di chuyển của đạn
            self._update_bullets()
            # Update màn hình mới
            self._update_screen()
    
    # Hàm kiểm tra các sự kiện như ấn nút hay thoát game
    def _check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
    
    # Hàm kiểm tra thao tác nhấn phím
    def _check_keydown_event(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True 
        elif event.key == pygame.K_s:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            exit()
    
    # Hàm kiểm tra thao tác nhấc phím
    def _check_keyup_event(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # Hàm lưu các biến bullet được tạo ra đưa vào group bullets đã tạo
    def _fire_bullet(self):
        # kiểm tra xem số đạn trên màn hình có vượt quá số đạn cho phép không
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    # Hàm cập nhật đạn
    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    # Hàm cập nhật màn hình sau các vòng lặp
    def _update_screen(self):
        # Đổ màu nền
        self.screen.blit(self.bg_color, (0, 0))
        # Vẽ con tàu
        self.ship.blitme()
        # Thực hiện vẽ các bullet đã được lưu
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Vẽ lại cửa sổ mới sau khi cập nhật
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()