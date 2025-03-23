import pygame.font

class Button:
    def __init__(self, ai_game, msg, x, y, button_color=None):
        """Инициализирует атрибуты кнопки."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Настройки кнопки
        self.width, self.height = 200, 50
        self.button_color = button_color if button_color else (0, 255, 0)  # Зеленый по умолчанию
        self.text_color = (255, 255, 255)  # Белый цвет текста
        self.font = pygame.font.SysFont(None, 48)

        # Создание прямоугольника кнопки и выравнивание
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)

        # Сообщение на кнопке
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Преобразует текст в изображение и центрирует его на кнопке."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self, mouse_pos=None):
        """Отрисовывает кнопку на экране."""
        if mouse_pos and self.rect.collidepoint(mouse_pos):
            # Изменение цвета при наведении
            self.screen.fill(
                (min(self.button_color[0] + 50, 255),  # Ограничение значения цвета до 255
                min(self.button_color[1] + 50, 255),
                min(self.button_color[2] + 50, 255)
            ),
                self.rect
            )
        else:
            self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)