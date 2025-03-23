import pygame
import random
from pygame.sprite import Sprite  

class Star(Sprite):  
    """Класс для создания звезд"""

    def __init__(self, screen_width, screen_height):
        super().__init__()  
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Создаем поверхность для звезды
        self.size = random.randint(1, 3)  # Случайный размер звезды
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)  # Прозрачная поверхность
        self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        pygame.draw.circle(self.image, self.color, (self.size, self.size), self.size)  

        # Позиция звезды
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width)  # Случайная позиция по X
        self.rect.y = random.randint(0, screen_height)  # Случайная позиция по Y

        # Скорость звезды
        self.speed = random.randint(1, 3)  # Случайная скорость звезды

    def update(self):
        """Обновляет позицию звезды"""
        self.rect.y += self.speed  # Звезды движутся вниз
        if self.rect.y > self.screen_height:  # Если звезда ушла за пределы экрана
            self.rect.y = 0  # Возвращаем ее в начало
            self.rect.x = random.randint(0, self.screen_width)  # Случайная позиция по X


