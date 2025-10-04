import pygame
from sys import exit
from settings import Settings
from ship import Ship 
from bullet import Bullet 
from alien import Alien 
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
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

        # Lưu đạn vào một nhóm
        self.bullets = pygame.sprite.Group()
        
        # Lưu alien vào một nhóm như bullet
        self.aliens = pygame.sprite.Group()

        # 
        self.stats = GameStats(self)

        # Khởi tạo hàm hiển thị điểm số
        self.sb = Scoreboard(self)

        # Khởi tạo hàm cài đặt alien
        self._create_fleet()

        # Khởi tạo button Play
        self.play_button = Button(self, "Play")

        # Cài đặt background
        self.bg_color = pygame.image.load('D:/pythonLabICN/Alien Invasion remake/images/bg.jpg')
        self.bg_color = pygame.transform.scale(self.bg_color, (self.settings.screen_width, self.settings.screen_height))
    
    # Hàm chạy game
    def run_game(self):
        while True:
            # Check các sự kiện
            self._check_event()
            
            if self.stats.game_active:
                # update hoạt động của con tàu
                self.ship.update()
                # update đường di chuyển của đạn
                self._update_bullets()
                # Cập nhật vị trí alien
                self._update_aliens()
                
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    # Hàm kiểm tra thao tác nhấn phím
    def _check_keydown_event(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True 
        elif event.key == pygame.K_s:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self.stats.game_active = True 
        elif event.key == pygame.K_q:
            exit()
    
    # Hàm kiểm tra thao tác nhấc phím
    def _check_keyup_event(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    # Hàm kiểm tra khi ấn button Play
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset lại các thông số game
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True

            # Xóa hết alien và bullet còn sót lại
            self.aliens.empty()
            self.bullets.empty()

            # Tạo lại fleet và đặt con tàu về vị trí ban đầu
            self._create_fleet()
            self.ship.center_ship()
            # Ẩn con trỏ chuột
            pygame.mouse.set_visible(False)

            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_hearts()
            
    # Ship bị va vào alien
    def _ship_hit(self):
        if self.settings.ship_limit > 0:
            # Trừ mạng khi tàu va alien
            self.stats.ship_left -= 1
            self.sb.prep_hearts()
            # Xóa hết alien và bullet xuất hiện trên màn hình khi va chạm
            self.aliens.empty()
            self.bullets.empty()

            # Tạo alien mới và đặt ship lại vị trí ban đầu
            self._create_fleet()
            self.ship.center_ship()

            # Pause 1s 
            sleep(1)
        else:
            self.stats.game_active = False
    
    # Hàm lưu các biến bullet được tạo ra đưa vào group bullets đã tạo
    def _fire_bullet(self):
        # kiểm tra xem số đạn trên màn hình có vượt quá số đạn cho phép không
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    # Hàm cập nhật vị trí đạn
    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()
    
    # Hàm set up khi đạn bán trúng alien khi hết sạch alien tạo fleet mới
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Tăng level
            self.stats.level += 1
            self.sb.prep_level()
        
        # Tăng điểm số
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

    # Hàm tạo alien 
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # Tính khoảng trống có thể để tạo alien trên một hàng
        available_space_x = self.settings.screen_width - 2*alien_width
        # Tính xem có thể setup tối đa bao nhiêu alien
        number_of_aliens = available_space_x // (2*alien_width)

        # 
        number_of_rows = (self.settings.screen_height - (6*alien_height) - self.ship.rect.height) // (2*alien_height)
        for row_number in range(number_of_rows):
            for alien_number in range(number_of_aliens):
                self._create_alien(row_number, alien_number, alien_width, alien_height)

    # Hàm tạo một hàng alien
    def _create_alien(self, row_number, alien_number, alien_width, alien_height):
        alien = Alien(self)
        alien.x = alien_width + 2*alien_width*alien_number # tọa độ x phụ thuộc vào đây là alien thứ mấy
        alien.rect.x = alien.x 
        alien.rect.y = alien_height + 2* alien_height* row_number # tọa độ y phụ thuộc vào đây là row thứ mấy
        self.aliens.add(alien)

    # Nếu một hàng alien chạm vào bottom thì cũng như ship bị chạm
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break 
    
    # Cập nhật di chuyển của alien
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        # Cập nhật alien khi va chạm
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    # Hàm kiểm tra xem alien có trạm vào cạnh bên của screen hay không
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    # Hàm điều hướng cho fleet dịch xuống và đổi hướng di chuyển của alien
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    # Hàm cập nhật màn hình sau các vòng lặp
    def _update_screen(self):
        # Đổ màu nền
        self.screen.blit(self.bg_color, (0, 0))
        # Vẽ con tàu
        self.ship.blitme()
        # Thực hiện vẽ các bullet đã được lưu
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Hiển thị điểm số
        self.sb.show_score()
        # Vẽ button Play nếu game không hoạt động
        if not self.stats.game_active:
            self.play_button.draw_button()
        # Vẽ lại cửa sổ mới sau khi cập nhật
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()