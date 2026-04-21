import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL_SIZE, 0)

score = 0
level = 1
foods_eaten = 0
speed = 7


def generate_food():
    while True:
        x = random.randint(1, (WIDTH // CELL_SIZE) - 2) * CELL_SIZE
        y = random.randint(1, (HEIGHT // CELL_SIZE) - 2) * CELL_SIZE

        if (x, y) not in snake:
            weight = random.choice([1, 2, 3])
            return (x, y, weight)


food = generate_food()

food_spawn_time = pygame.time.get_ticks()
food_lifetime = 4000  


def draw_snake():
    for block in snake:
        pygame.draw.rect(screen, GREEN, (*block, CELL_SIZE, CELL_SIZE))


def move_snake():
    head_x, head_y = snake[0]
    dx, dy = direction

    new_head = (head_x + dx, head_y + dy)

    snake.insert(0, new_head)
    snake.pop()


def check_collision():
    head_x, head_y = snake[0]

    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        return True

    if snake[0] in snake[1:]:
        return True

    return False


def level_up():
    global level, speed
    level += 1
    speed += 2


running = True

while running:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                direction = (-CELL_SIZE, 0)
            if event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                direction = (CELL_SIZE, 0)
            if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                direction = (0, -CELL_SIZE)
            if event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                direction = (0, CELL_SIZE)

    move_snake()

    if check_collision():
        pygame.time.delay(1000)
        pygame.quit()
        sys.exit()

    food_rect = pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE)

    if snake[0] == (food[0], food[1]):
        snake.append(snake[-1])  

        score += food[2]         
        foods_eaten += 1

        food = generate_food()
        food_spawn_time = pygame.time.get_ticks()  

        if foods_eaten % 3 == 0:
            level_up()

    if pygame.time.get_ticks() - food_spawn_time > food_lifetime:
        food = generate_food()
        food_spawn_time = pygame.time.get_ticks()

    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

    draw_snake()

    text = font.render(f"Score: {score}  Level: {level}", True, BLACK)
    screen.blit(text, (10, 10))

    pygame.display.update()