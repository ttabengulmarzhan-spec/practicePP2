import pygame
import sys
import random

pygame.init()

FPS = 60
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

font = pygame.font.SysFont("Verdana", 20)

enemy_speed = 5
coins_collected = 0

speed_level = 0
LEVEL_UP = 5   


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/gulmarzantaben/Desktop/practicePP2/Practice10/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (200, 500)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(5, 0)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/gulmarzantaben/Desktop/practicePP2/Practice10/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, enemy_speed)

        if self.rect.top > HEIGHT:
            self.respawn()

    def respawn(self):
        self.rect.top = 0
        self.rect.center = (random.randint(40, WIDTH - 40), 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("/Users/gulmarzantaben/Desktop/practicePP2/Practice10/coin.gif")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), -50)

        self.weight = random.choice([1, 2, 3])

    def move(self):
        self.rect.move_ip(0, 5)

        if self.rect.top > HEIGHT:
            self.respawn()

    def respawn(self):
        self.rect.top = -50
        self.rect.center = (random.randint(40, WIDTH - 40), -50)
        self.weight = random.choice([1, 2, 3])  


player = Player()
enemy = Enemy()

coins = pygame.sprite.Group()
for _ in range(3):   
    coins.add(Coin())

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(coins)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.move()
    enemy.move()

    for coin in coins:
        coin.move()

    if pygame.sprite.collide_rect(player, enemy):
        screen.fill(RED)
        pygame.display.update()
        pygame.time.delay(1500)
        pygame.quit()
        sys.exit()

    for coin in coins:
        if pygame.sprite.collide_rect(player, coin):
            coins_collected += coin.weight
            coin.respawn()

            if coins_collected // LEVEL_UP > speed_level:
                speed_level += 1
                enemy_speed += 1

    screen.fill(WHITE)

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    score_text = font.render(
        f"Coins: {coins_collected} | Speed: {enemy_speed}",
        True,
        BLACK
    )
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(FPS)