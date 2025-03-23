import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star 
from button import Button
from alien import Alien, FastAlien, StrongAlien, BossAlien   
import random



# Создание пользовательского события для паузы
PAUSE_EVENT = pygame.USEREVENT + 1

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()

        # Загрузка звуков
        self.laser_sound = pygame.mixer.Sound('sounds/laser.mp3')
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion.mp3')
        self.background_music = pygame.mixer.Sound('sounds/background.mp3')
        # Воспроизведение фоновой музыки
        self.background_music.play(-1)

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

            # Центр экрана
        center_x = self.settings.screen_width // 2
        center_y = self.settings.screen_height // 2


        # Создание кнопок для главного меню
        self.play_button = Button(self, "Play", center_x, center_y - 100, (0, 128, 255))  # Синий цвет
        

        #Создание экземпляра для хранение игровой статистики
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self.screen, self.settings)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()  # Группа для звезд

        self._create_stars()  # Создание звезд
        self._create_fleet()
        
       

    def _create_stars(self):
        """Создает звездное небо"""
        for _ in range(50):  
            star = Star(self.settings.screen_width, self.settings.screen_height)
            self.stars.add(star)

    def _create_fleet(self):
        """Создает флот пришельцев."""
        alien_types = [Alien, FastAlien, StrongAlien]  # Типы пришельцев
        if self.stats.level % 5 == 0:  # Каждый 5-й уровень — босс
            alien_types = [BossAlien]
            boss = BossAlien(self)
            boss.rect.centerx = self.settings.screen_width // 2  # Центр экрана по X
            boss.rect.y = 50  # Позиция по Y (вверху экрана)
            self.aliens.add(boss)
            return  # Завершаем метод, так как босс создан



        alien = alien_types[0](self)  # Создаем пришельца (по умолчанию обычный)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                            (3 * alien_height) - ship_height)
        number_rows = 2

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                alien_type = random.choice(alien_types)  # Случайный тип пришельца
                self._create_alien(alien_number, row_number, alien_type)

    def _create_alien(self, alien_number, row_number, alien_type):
        """Создает пришельца и размещает его в ряду."""
        alien = alien_type(self)  # Создаем пришельца выбранного типа
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
        



    def _check_fleet_edges(self):
        """Реагирует на достижение пришельца края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_bullets(self):
        """Обновляет позиции снарядов и проверяет столкновения."""
        self.bullets.update()  # Обновление позиций снарядов

        # Удаление снарядов, вышедших за пределы экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
               self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)
        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    if hasattr(alien, 'health'):  # Если у пришельца есть здоровье
                        alien.health -= 1
                        if alien.health <= 0:  # Удаляем пришельца, если здоровье <= 0
                            self.aliens.remove(alien)
                            self.stats.score += alien.points
                    else:
                        self.aliens.remove(alien)  # Удаляем пришельца без здоровья
                        self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()
        
            if not self.aliens:
                # Уничтожение существующих снарядов и создание нового флота
                self.bullets.empty()
                self._create_fleet()
                self.settings.increase_speed()  

                # Увеличение уровня
                self.stats.level += 1
                self.sb.prep_level()

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
            self._update_stars()  
            self._update_screen()

    def _remove_old_bullets(self):
        """Удаляет снаряды, вышедшие за пределы экрана."""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == PAUSE_EVENT:  # Обработка события паузы
                pygame.time.set_timer(PAUSE_EVENT, 0)  # Остановка таймера
                self.stats.game_active = True  # Возобновление игры
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Обработка нажатия Enter
                    self._check_play_button(self.play_button.rect.center)
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
                   
    def _check_difficulty_buttons(self, mouse_pos):
        """Обрабатывает нажатия кнопок выбора уровня сложности."""
        if self.easy_button.rect.collidepoint(mouse_pos):
            self.settings.set_difficulty("easy")
        elif self.medium_button.rect.collidepoint(mouse_pos):
            self.settings.set_difficulty("medium")
        elif self.hard_button.rect.collidepoint(mouse_pos):
            self.settings.set_difficulty("hard")

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Сброс игровых настроек
            self.settings.initialize_dynamic_settings()
            # Сброс игровой статистики
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #Указатель мыши скрывается
            pygame.mouse.set_visible(False)

            #Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создает новый снаряд, если их меньше определенного количества."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self.screen, self.settings, self.ship)
            self.bullets.add(new_bullet)
            self.laser_sound.play()

        

    def _update_stars(self):
        """Обновляет позиции звезд."""
        self.stars.update()  # Обновляем все звезды одновременно

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте."""
        self._check_fleet_edges()  # Проверка достижения края экрана
        self.aliens.update()  # Обновление позиций пришельцев
        

        # Проверка коллизий "пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Проверка, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Обрабатывает столкновение коробля с пришельцем"""
        if self.stats.ships_left > 0:
            #Уменьшение ships_left и обновление панели счета.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # Установка таймера для паузы
            pygame.time.set_timer(PAUSE_EVENT, 500)  # 500 миллисекунд = 0.5 секунды
            self.stats.game_active = False  # Приостановка игры
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """Проверяет добрались ли пришельцы до нижн края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Происходит то же что и при столкновении с кораблем.
                self._ship_hit()
                break
       

    def _update_screen(self):
        """Обновляет изображение на экране и отображает новый экран."""
        self.screen.fill(self.settings.bg_color)  # Заливка экрана цветом фона

        # Отрисовка звезд
        self.stars.draw(self.screen)

        # Отрисовка корабля
        self.ship.blitme()

        # Отрисовка снарядов
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Отрисовка пришельцев
        self.aliens.draw(self.screen)
        

        # Вывод информации о счете
        self.sb.show_score()

        # Получение позиции мыши
        mouse_pos = pygame.mouse.get_pos()

        
        # Отрисовка кнопки Play, если игра не активна
        if not self.stats.game_active:
            self.play_button.draw_button(mouse_pos)
        


        pygame.display.flip()

if __name__ == "__main__":
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()