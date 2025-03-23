import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, screen, settings, ship):
        super().__init__()
        self.screen = screen
        self.settings = settings

        # Создание снаряда в позиции корабля
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.midtop = ship.rect.midtop

        # Инициализация координаты y как числа
        self.y = float(self.rect.y)

    def update(self):
        """Обновляет позицию снаряда."""
        self.y -= self.settings.bullet_speed_factor  # Движение снаряда вверх
        self.rect.y = int(self.y)  # Преобразуем в int, так как rect.y требует целых чисел

        # Удаление снарядов, вышедших за пределы экрана
        if self.rect.bottom < 0:
            self.kill()  # Удаляем снаряд из группы

    def draw_bullet(self):
        """Рисует снаряд на экране."""
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)