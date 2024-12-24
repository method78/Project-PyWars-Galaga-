import pygame
import sys
import math
from random import randint

pygame.init()

width, height = 1000, 450
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyWars")

background_color = (0, 0, 0)

# Изменяем пути к изображениям, добавляя папку "images"
main_bullet_image = pygame.image.load("images/bullet.jpg")
enemy_bullet_image = pygame.image.load("images/bullet2.png")
warrior_image = pygame.image.load("images/warrior.png")
shotgun_image = pygame.image.load("images/shotgun.png")
game_over_image = pygame.image.load("images/game_over.jpg")
boom_image = pygame.image.load("images/boom.jpg")
coin_image = pygame.image.load("images/coin.png")  # Загружаем изображение монеты

game_over_rect = game_over_image.get_rect(center=(-500, 250))
warrior_rect = warrior_image.get_rect(center=(50, 250))

speed = 10
main_bullet_speed = 5  # Увеличенная скорость пуль персонажа
initial_enemy_bullet_speed = 7  # Начальная скорость пуль врагов
enemy_bullet_speed = initial_enemy_bullet_speed  # Текущая скорость пуль врагов
target = None
end = False

# Позиции для пушек (7 пушек с вертикальным отступом)
shotgun_positions = [(width - 100, 10 + i * 60) for i in range(7)]  # 7 пушек с вертикальным отступом

# Таймеры для пушек
shotgun_timers = [randint(2000, 5000) for _ in range(7)]
last_shot_time = [0] * 7  # Время последнего выстрела для каждой пушки

# Переменные для таймера
survival_time = 0  # Время выживания в миллисекундах
font = pygame.font.Font(None, 36)  # Шрифт для отображения времени

# Состояние пушек (1 - активна, 0 - уничтожена)
shotgun_states = [1] * 7
wave_count = 0
reset_time = 7000  # Время, через которое пушки восстанавливаются после уничтожения
reset_timer = 0

# Переменные для пуль
max_bullets = 8  # Максимальное количество пуль за волну
current_bullets = 0  # Текущее количество пуль

# Переменные для монет
coin = None  # Монета
coin_timer = 0  # Таймер для монеты
coin_duration = 5000  # Длительность появления монеты (в миллисекундах)
coins_collected = 0  # Счетчик собранных монет

def move_towards_target(rect, target_x, target_y):
    dx = target_x - rect.centerx
    dy = target_y - rect.centery
    distance = math.sqrt(dx ** 2 + dy ** 2)

    if distance > 0:
        dx /= distance
        dy /= distance
        rect.x += dx * speed
        rect.y += dy * speed

    return rect

def main():
    global warrior_rect, warrior_image, target, main_bullet_image, width, boom_image, end, survival_time
    global shotgun_states, wave_count, reset_timer, current_bullets, enemy_bullet_speed
    global coin, coin_timer, coins_collected, coin_duration

    clock = pygame.time.Clock()
    MYEVENTTYPE = pygame.USEREVENT + 1  # событие движения пуль и выстрелов пушек
    MYEVENTTYPE2 = pygame.USEREVENT + 2  # событие выхода таблички game over
    pygame.time.set_timer(MYEVENTTYPE, 1)
    pygame.time.set_timer(MYEVENTTYPE2, 1)
    list_main_bullets = []
    list_enemy_bullets = []

    while True:
        current_time = pygame.time.get_ticks()  # Получаем текущее время в миллисекундах

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                target = event.pos
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and current_bullets < max_bullets:
                    bullet_rect = main_bullet_image.get_rect(
                        center=(warrior_rect.centerx + 30, warrior_rect.centery + 10))
                    list_main_bullets.append(bullet_rect)
                    current_bullets += 1  # Увеличиваем количество пуль

            if event.type == MYEVENTTYPE and not end:
                for i in range(len(shotgun_positions)):
                    # Проверяем, можно ли стрелять из пушки
                    if shotgun_states[i] == 1 and current_time - last_shot_time[i] >= shotgun_timers[i]:
                        # Создаем пулю врага
                        enemy_bullet = enemy_bullet_image.get_rect(
                            center=(width - 100, shotgun_positions[i][1] + 30))  # Стреляем из i-й пушки
                        enemy_bullet.width *= 3  # Увеличиваем ширину пули врага
                        enemy_bullet.height *= 3  # Увеличиваем высоту пули врага
                        list_enemy_bullets.append(enemy_bullet)
                        last_shot_time[i] = current_time  # Обновляем время последнего выстрела
                        # Случайно обновляем таймер для следующего выстрела
                        shotgun_timers[i] = randint(1000, 2000)

                # Двигаем главные пули
                for bullet in list_main_bullets:
                    bullet.centerx += main_bullet_speed  # Используем новую скорость для главных пуль

            if event.type == MYEVENTTYPE2 and end:
                if game_over_rect.centerx != 500:
                    game_over_rect.centerx += 1

        screen.fill(background_color)

        if target and not end:
            if target[0] > 800:
                warrior_rect = move_towards_target(warrior_rect, 800, target[1])
            else:
                warrior_rect = move_towards_target(warrior_rect, target[0], target[1])
            if math.hypot(target[0] - warrior_rect.centerx, target[1] - warrior_rect.centery) < speed:
                target = None

        screen.blit(warrior_image, warrior_rect)
        screen.blit(game_over_image, game_over_rect)
        if list_main_bullets and not end:
            for bullet in list_main_bullets:
                screen.blit(main_bullet_image, bullet)

        # Обновление и отрисовка пуль врагов
        if list_enemy_bullets and not end:
            for bullet in list_enemy_bullets:
                bullet.centerx -= enemy_bullet_speed  # Двигаем пулю врага влево с заданной скоростью
                if abs(bullet.centerx - warrior_rect.centerx) < 25 and abs(bullet.centery - warrior_rect.centery) < 25:
                    # событие встречи корабля с пулей (смерть)
                    end = True
                    warrior_image = boom_image
                screen.blit(enemy_bullet_image, bullet)

        # Проверка попадания пуль героя в пули врага
        for bullet in list_main_bullets[:]:  # Используем срез, чтобы избежать изменения во время итерации
            for enemy_bullet in list_enemy_bullets[:]:
                if bullet.colliderect(enemy_bullet):  # Если пуля героя попадает в пулю врага
                    list_main_bullets.remove(bullet)  # Удаляем пулю героя
                    list_enemy_bullets.remove(enemy_bullet)  # Удаляем пулю врага
                    current_bullets -= 1  # Уменьшаем счетчик пуль
                    break  # Выходим из цикла, чтобы не изменять коллекцию во время итерации

        # Проверка попадания пуль героя в пушки
        for bullet in list_main_bullets[:]:  # Используем срез, чтобы избежать изменения во время итерации
            for i in range(len(shotgun_positions)):
                if shotgun_states[i] == 1:  # Если пушка активна
                    shotgun_rect = shotgun_image.get_rect(topleft=shotgun_positions[i])  # Положение пушки
                    if bullet.colliderect(shotgun_rect):
                        shotgun_states[i] = 0  # Уничтожаем пушку
                        list_main_bullets.remove(bullet)  # Удаляем пулю
                        current_bullets -= 1  # Уменьшаем счетчик пуль
                        break  # Выходим из цикла, чтобы не изменять коллекцию во время итерации

        # Отрисовка пушек в верхнем правом углу
        for i, pos in enumerate(shotgun_positions):
            if shotgun_states[i] == 1:  # Если пушка активна, отрисовываем ее
                shotgun_rect = shotgun_image.get_rect(topleft=pos)  # Положение пушки
                screen.blit(shotgun_image, shotgun_rect)

        # Проверка на уничтожение всех пушек
        if all(state == 0 for state in shotgun_states):  # Если все пушки уничтожены
            reset_timer += 1  # Увеличиваем таймер
            if reset_timer >= reset_time / 1000:  # Если прошло 7 секунд
                shotgun_states = [1] * 7  # Восстанавливаем все пушки
                reset_timer = 0  # Сбрасываем таймер
                wave_count += 1  # Увеличиваем счетчик волн
                current_bullets = 0  # Сбрасываем количество пуль при начале новой волны

                # Появление монеты после волны
                coin = coin_image.get_rect(center=(randint(0, 500), randint(0, 450)))  # Случайные координаты для монеты
                coin_timer = current_time  # Сброс таймера монеты

                enemy_bullet_speed *= 1.2  # Увеличиваем скорость пуль врагов

        # Обновление и отображение монеты
        if coin is not None:
            if current_time - coin_timer < coin_duration:  # Если монета еще не исчезла
                screen.blit(coin_image, coin)
                # Проверка касания монеты
                if warrior_rect.colliderect(coin):
                    coins_collected += 1  # Увеличиваем счетчик монет
                    coin = None  # Удаляем монету
            else:
                coin = None  # Удаляем монету, если время вышло

        # Обновляем и отображаем таймер и количество пуль
        if not end:
            survival_time = current_time // 1000  # Переводим время в секунды
            timer_surface = font.render(f"Время жизни: {survival_time}s", True, (255, 255, 255))
            wave_surface = font.render(f"Волна: {wave_count}", True, (255, 255, 255))
            screen.blit(timer_surface, (10, 10))  # Отображаем таймер
            screen.blit(wave_surface, (10, 50))  # Отображаем номер волны

            # Отображаем количество пуль
            bullet_count_surface = font.render(f"Пули: {current_bullets}/{max_bullets}", True, (255, 255, 255))
            screen.blit(bullet_count_surface, (10, 90))  # Отображаем количество пуль

            # Отображаем количество монет
            coins_surface = font.render(f"Монеты: {coins_collected}", True, (255, 255, 255))
            screen.blit(coins_surface, (10, 130))  # Отображаем количество монет

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
