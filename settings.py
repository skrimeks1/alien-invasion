class Settings:
    
    """Класс для хранения всех настроек Alien Invasion."""

    def __init__(self):
        """Инициализирует статические настройки игры."""
        # Параметры экрана
        self.screen_width = 1366
        self.screen_height = 768
        self.bg_color = (25, 25, 112)  # Темно-синий цвет фона

        # Настройки корабля
        self.ship_limit = 3  # Количество жизней корабля
        self.ship_speed_factor = 1.5  # Скорость корабля (будет изменяться)

        # Параметры снаряда
        self.bullet_width = 5  # Ширина снаряда
        self.bullet_height = 15  # Высота снаряда
        self.bullet_color = (140, 140, 140)  # Серый цвет снаряда
        self.bullets_allowed = 3  # Максимальное количество снарядов на экране
        self.bullet_speed_factor = 3.0  # Скорость снаряда (будет изменяться)

        # Настройки пришельцев
        self.alien_speed_factor = 1.0  # Скорость пришельцев (будет изменяться)
        self.fleet_drop_speed = 15  # Скорость опускания флота пришельцев
        self.fleet_direction = 1  # 1 означает движение вправо, -1 — влево

        # Темп ускорения игры
        self.speedup_scale = 1.1  # Коэффициент увеличения скорости
        # Темп роста стоимости пришельцев
        self.score_scale = 1.5

        # Уровни сложности
        self.difficulty_level = "easy"  # По умолчанию: легкий уровень

        # Инициализация динамических настроек
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 1.0
        self.fleet_direction = 1
        
        # Подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        """Увеличивает настройки скорости и стоимости пришельцев"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    def set_difficulty(self, difficulty):
        """Устанавливает уровень сложности."""
        self.difficulty_level = difficulty
        if difficulty == "easy":
            self.ship_speed_factor = 1.5
            self.bullet_speed_factor = 3.0
            self.alien_speed_factor = 1.0
            self.ship_limit = 3
        elif difficulty == "medium":
            self.ship_speed_factor = 2.0
            self.bullet_speed_factor = 2.5
            self.alien_speed_factor = 1.5
            self.ship_limit = 2
        elif difficulty == "hard":
            self.ship_speed_factor = 2.5
            self.bullet_speed_factor = 2.0
            self.alien_speed_factor = 2.0
            self.ship_limit = 1