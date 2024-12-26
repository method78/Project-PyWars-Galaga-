import pygame
import sys
import math
from random import randint

pygame.init()

width, height = 1000, 450
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyWars_v1.0")

background_color = (0, 0, 0)

main_bullet_image = pygame.image.load("images/bullet.jpg")
enemy_bullet_image = pygame.image.load("images/bullet2.png")
warrior_image = pygame.image.load("images/warrior.png")
shotgun_image = pygame.image.load("images/shotgun.png")
game_over_image = pygame.image.load("images/game_over.jpg")
boom_image = pygame.image.load("images/boom.jpg")
coin_image = pygame.image.load("images/coin.png")


class Player:
    def __init__(self):
        self.image = warrior_image
        self.rect = self.image.get_rect(center=(50, 250))
        self.speed = 10
        self.current_bullets = 0
        self.max_bullets = 8

    def move_towards(self, target):
        if target is not None:
            dx = target[0] - self.rect.centerx
            dy = target[1] - self.rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance > 0:
                dx /= distance
                dy /= distance
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
                if math.sqrt((self.rect.centerx - target[0]) ** 2 + (self.rect.centery - target[1]) ** 2) < self.speed:
                    self.rect.center = target


class Bullet:
    def __init__(self, image, center):
        self.image = image
        self.rect = self.image.get_rect(center=center)

    def update(self, speed):
        self.rect.centerx += speed


class Shotgun:
    def __init__(self, position):
        self.image = shotgun_image
        self.position = position
        self.state = 1
        self.last_shot_time = 0
        self.timer = randint(2000, 5000)

    def shoot(self, current_time):
        if self.state == 1 and current_time - self.last_shot_time >= self.timer:
            self.last_shot_time = current_time
            self.timer = randint(1000, 2000)
            return Bullet(enemy_bullet_image, (self.position[0], self.position[1] + 30))
        return None


class Coin:
    def __init__(self):
        self.image = coin_image
        self.rect = None
        self.timer = 0
        self.duration = 5000

    def spawn(self):
        self.rect = self.image.get_rect(center=(randint(0, 500), randint(0, 450)))
        self.timer = pygame.time.get_ticks()

    def is_active(self):
        return self.rect is not None and (pygame.time.get_ticks() - self.timer < self.duration)

    def collect(self):
        self.rect = None


class HUD:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)

    def draw(self, survival_time, wave_count, coins_collected, current_bullets, max_bullets):
        timer_surface = self.font.render(f"Время жизни: {survival_time}s", True, (255, 255, 255))
        wave_surface = self.font.render(f"Волна: {wave_count}", True, (255, 255, 255))
        bullet_count_surface = self.font.render(f"Пули: {current_bullets}/{max_bullets}", True, (255, 255, 255))
        coins_surface = self.font.render(f"Монеты: {coins_collected}", True, (255, 255, 255))
        screen.blit(timer_surface, (10, 10))
        screen.blit(wave_surface, (10, 50))
        screen.blit(bullet_count_surface, (10, 90))
        screen.blit(coins_surface, (10, 130))


def main():
    global end, wave_count, reset_timer, enemy_bullet_speed, coins_collected

    clock = pygame.time.Clock()
    MYEVENTTYPE = pygame.USEREVENT + 1
    MYEVENTTYPE2 = pygame.USEREVENT + 2
    pygame.time.set_timer(MYEVENTTYPE, 1)
    pygame.time.set_timer(MYEVENTTYPE2, 1)

    player = Player()
    shotguns = [Shotgun((width - 100, 10 + i * 60)) for i in range(7)]
    coins_collected = 0
    coin = Coin()
    end = False
    wave_count = 0
    reset_timer = 0
    enemy_bullet_speed = 7

    list_main_bullets = []
    list_enemy_bullets = []

    game_over_rect = game_over_image.get_rect(center=(-500, 250))
    target = None
    hud = HUD()

    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not end:
                target = event.pos
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.current_bullets < player.max_bullets:
                    bullet = Bullet(main_bullet_image, (player.rect.centerx + 30, player.rect.centery + 10))
                    list_main_bullets.append(bullet)
                    player.current_bullets += 1
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if player.rect.centery - 40 > 0:
                        target = (player.rect.centerx, player.rect.centery - 40)
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if player.rect.centery + 40 < 450:
                        target = (player.rect.centerx, player.rect.centery + 40)
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if player.rect.centerx - 40 > 0:
                        target = (player.rect.centerx - 40, player.rect.centery)
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if player.rect.centerx + 40 < 800:
                        target = (player.rect.centerx + 40, player.rect.centery)
                # if event.key == pygame.K_f:  # restart
                #     main()
                #     return
            if event.type == MYEVENTTYPE and not end:
                for shotgun in shotguns:
                    bullet = shotgun.shoot(current_time)
                    if bullet:
                        list_enemy_bullets.append(bullet)

                for bullet in list_main_bullets:
                    bullet.update(5)

            if event.type == MYEVENTTYPE2 and end:
                if game_over_rect.centerx != 500:
                    game_over_rect.centerx += 1

        screen.fill(background_color)

        if not end:
            player.move_towards(target)
            screen.blit(player.image, player.rect)

            for bullet in list_main_bullets:
                bullet.update(5)
                screen.blit(bullet.image, bullet.rect)

            for bullet in list_enemy_bullets:
                bullet.update(-enemy_bullet_speed)
                if bullet.rect.colliderect(player.rect):
                    end = True
                    player.image = boom_image
                screen.blit(bullet.image, bullet.rect)

            for bullet in list_main_bullets[:]:
                for enemy_bullet in list_enemy_bullets[:]:
                    if bullet.rect.colliderect(enemy_bullet.rect):
                        list_main_bullets.remove(bullet)
                        list_enemy_bullets.remove(enemy_bullet)
                        player.current_bullets -= 1
                        break

            for bullet in list_main_bullets[:]:
                for shotgun in shotguns:
                    if shotgun.state == 1:
                        shotgun_rect = shotgun.image.get_rect(topleft=shotgun.position)
                        if bullet.rect.colliderect(shotgun_rect):
                            shotgun.state = 0
                            list_main_bullets.remove(bullet)
                            player.current_bullets -= 1
                            break

            for shotgun in shotguns:
                if shotgun.state == 1:
                    screen.blit(shotgun.image, shotgun.image.get_rect(topleft=shotgun.position))

            if all(shotgun.state == 0 for shotgun in shotguns):
                reset_timer += 1
                if reset_timer >= 7000 / 1000:
                    for shotgun in shotguns:
                        shotgun.state = 1
                    reset_timer = 0
                    wave_count += 1
                    player.current_bullets = 0
                    coin.spawn()
                    enemy_bullet_speed *= 1.2

            if coin.is_active():
                screen.blit(coin.image, coin.rect)
                if player.rect.colliderect(coin.rect):
                    coins_collected += 1
                    coin.collect()

            survival_time = current_time // 1000
            hud.draw(survival_time, wave_count, coins_collected, player.current_bullets, player.max_bullets)

        else:
            screen.blit(game_over_image, game_over_rect)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
