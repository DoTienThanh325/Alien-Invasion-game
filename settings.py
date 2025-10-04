class Settings:
    def __init__(self):
        # Cài đặt mặc định cho giao diện màn hình game
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Tạo biến tốc độ tàu bay
        self.ship_limit = 5

        # Cài đặt mặc định cho đạn
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 'red'
        self.bullet_allowed = 5

        # Alien setting
        self.fleet_drop_speed = 5.0
        self.fleet_direction = 1

        # Tăng tốc game
        self.speedup_scale = 1.1
        # Tăng điểm số
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0
        self.fleet_direction = 1
        
        # Điểm số
        self.alien_points = 50
    
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
