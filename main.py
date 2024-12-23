import pygame
import sys
import math
from random import randint

pygame.init()

width, height = 1000, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyWars_v1.0")

background_color = (0, 0, 0)

main_bullet_image = pygame.image.load("images/main_bullet.png")
warrior_image = pygame.image.load("images/warrior.png")
shotgun_image = pygame.image.load("images/enemy.jpg")  # Загрузка изображения дробовика

warrior_rect = warrior_image.get_rect(center=(50, 250))
list_enemies = []
for _ in range(2):
    for _ in range(10):
        pass  # создание врагов (пушек)

speed = 10
target = None

# Позиции для пушек (7 пушек с вертикальным отступом)
shotgun_positions = [(width - 100, 10 + i * 60) for i in range(7)]  # 7 пушек с вертикальным отступом

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
    global warrior_rect, target, main_bullet_image
    clock = pygame.time.Clock()
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 1)
    MYEVENTTYPE2 = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE2, 50)
    list_main_bullets = []
    list_enemy_bullets = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                target = event.pos
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    list_main_bullets.append(main_bullet_image.get_rect(center=(warrior_rect.centerx + 30,
                                                                                warrior_rect.centery + 10)))
            if event.type == MYEVENTTYPE:
                for bullet in list_main_bullets:
                    bullet.centerx += 10
            if event.type == MYEVENTTYPE2:
                pass  # выстрел врагов каждые пол секунды

        screen.fill(background_color)

        if target:
            if target[0] > 800:
                warrior_rect = move_towards_target(warrior_rect, 800, target[1])
            else:
                warrior_rect = move_towards_target(warrior_rect, target[0], target[1])
            if math.hypot(target[0] - warrior_rect.centerx, target[1] - warrior_rect.centery) < speed:
                target = None

        screen.blit(warrior_image, warrior_rect)

        if list_main_bullets:
            for bullet in list_main_bullets:
                screen.blit(main_bullet_image, bullet)

        # Отрисовка дробовиков в верхнем правом углу
        for pos in shotgun_positions:
            shotgun_rect = shotgun_image.get_rect(topleft=pos)  # Положение дробовика
            screen.blit(shotgun_image, shotgun_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()