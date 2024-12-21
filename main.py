import pygame
import sys
import math

pygame.init()

width, height = 501, 501
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyWars_v1.0")

background_color = (0, 0, 0)

warrior_image = pygame.image.load("images/warrior.png")
warrior_rect = warrior_image.get_rect(center=(width // 2, height // 2))

speed = 5
target = None


def move_towards_target(rect, target_x, target_y):
    dx = target_x - rect.centerx
    dy = target_y - rect.centery
    distance = math.sqrt(dx**2 + dy**2)

    if distance > 0:
        dx /= distance
        dy /= distance
        rect.x += dx * speed
        rect.y += dy * speed

    return rect


def main():
    global warrior_rect, target
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                target = event.pos

        screen.fill(background_color)

        if target:
            warrior_rect = move_towards_target(warrior_rect, target[0], target[1])
            if math.hypot(target[0] - warrior_rect.centerx, target[1] - warrior_rect.centery) < speed:
                target = None

        screen.blit(warrior_image, warrior_rect)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
