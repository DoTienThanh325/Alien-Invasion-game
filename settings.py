class Settings:
    def __init__(self):
        # Cài đặt mặc định cho giao diện màn hình game
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Tạo biến tốc độ tàu bay
        self.ship_speed = 1.5

        # Cài đặt mặc định cho đạn
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 'red'
        self.bullet_allowed = 5