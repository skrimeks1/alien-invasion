import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Базовый класс для пришельцев."""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/alien.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def check_edges(self):
        """Возвращает True, если пришелец у края экрана."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        """Обновляет позицию пришельца."""
        self.x += self.settings.alien_speed_factor * self.settings.fleet_direction
        self.rect.x = self.x


class FastAlien(Alien):
    """Быстрый пришелец."""
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.speed_factor = 2.0  # Двигается быстрее
        self.points = 100  # Дает больше очков
        self.image = pygame.image.load('images/fast_alien.png')  
        self.image = pygame.transform.scale(self.image, (50, 50))


class StrongAlien(Alien):
    """Сильный пришелец."""
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.image = pygame.image.load('images/strong_alien.png')  
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.health = 3  # Требует 3 попадания для уничтожения
        self.points = 200  # Дает еще больше очков


class BossAlien(Alien):
    """Босс."""
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.image = pygame.image.load('images/boss.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.health = 20  # Много здоровья
        self.speed_factor = 0.5  # Медленный, но опасный
        self.points = 1000  # Очень много очков