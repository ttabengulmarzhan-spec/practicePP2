import random
import pygame

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

GRID_W = WIDTH // CELL_SIZE
GRID_H = HEIGHT // CELL_SIZE


WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GRAY = (200, 200, 200)

RED = (220, 50, 50)
DARK_RED = (150, 30, 30)

BLUE = (70, 130, 255)
ORANGE = (255, 170, 60)
PURPLE = (170, 80, 220)


class SnakeGame:
    def __init__(self, screen, settings, username, personal_best):
        self.screen = screen
        self.settings = settings
        self.username = username
        self.personal_best = personal_best

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 18)

        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = (CELL_SIZE, 0)

        self.score = 0
        self.level = 1
        self.foods_eaten = 0

        self.base_speed = 7
        self.speed_effect = None
        self.speed_effect_end = 0

        self.shield = False

        self.obstacles = set()

        self.food = None
        self.poison = None
        self.powerup = None

        self.spawn_food()
        self.spawn_poison()

        self.running = True

    def current_speed(self):
        speed = self.base_speed + (self.level - 1) * 2

        now = pygame.time.get_ticks()
        if self.speed_effect and now < self.speed_effect_end:
            if self.speed_effect == "boost":
                speed += 4
            elif self.speed_effect == "slow":
                speed = max(3, speed - 3)

        return speed

    def px_to_grid(self, x, y):
        return x // CELL_SIZE, y // CELL_SIZE

    def grid_to_px(self, gx, gy):
        return gx * CELL_SIZE, gy * CELL_SIZE

    def random_cell(self):
        while True:
            x = random.randint(0, GRID_W - 1)
            y = random.randint(0, GRID_H - 1)

            if (x, y) not in self.obstacles:
                return x, y

    def spawn_food(self):
        gx, gy = self.random_cell()
        x, y = self.grid_to_px(gx, gy)
        self.food = (x, y, random.choice([1, 2, 3]))

    def spawn_poison(self):
        gx, gy = self.random_cell()
        x, y = self.grid_to_px(gx, gy)
        self.poison = (x, y)

    def move(self):
        hx, hy = self.snake[0]
        dx, dy = self.direction

        new_head = (hx + dx, hy + dy)

        if not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            self.running = False
            return


        if new_head in self.snake:
            self.running = False
            return

        if self.px_to_grid(*new_head) in self.obstacles:
            self.running = False
            return

        self.snake.insert(0, new_head)

        if new_head == (self.food[0], self.food[1]):
            self.score += self.food[2]
            self.foods_eaten += 1
            self.spawn_food()
        else:
            self.snake.pop()

        if new_head == self.poison:
            if len(self.snake) > 2:
                self.snake.pop()
                self.snake.pop()
            else:
                self.running = False
            self.spawn_poison()

        if self.foods_eaten > 0 and self.foods_eaten % 3 == 0:
            self.level += 1

    def draw_grid(self):
        if not self.settings.get("grid", True):
            return

        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_grid()

        for gx, gy in self.obstacles:
            x, y = self.grid_to_px(gx, gy)
            pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))

        fx, fy, val = self.food
        pygame.draw.rect(self.screen, RED, (fx, fy, CELL_SIZE, CELL_SIZE))

        px, py = self.poison
        pygame.draw.rect(self.screen, DARK_RED, (px, py, CELL_SIZE, CELL_SIZE))


        base = self.settings.get("snake_color", [0, 200, 0])
        color = tuple(base)

        head_color = (
            max(0, color[0] - 40),
            max(0, color[1] - 40),
            max(0, color[2] - 40),
        )

        for i, (x, y) in enumerate(self.snake):
            c = head_color if i == 0 else color
            pygame.draw.rect(self.screen, c, (x, y, CELL_SIZE, CELL_SIZE))

        text = self.font.render(
            f"{self.username} | Score: {self.score} | Level: {self.level} | PB: {self.personal_best}",
            True,
            BLACK
        )
        self.screen.blit(text, (10, 10))

        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(self.current_speed())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return {"quit": True}

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.direction != (CELL_SIZE, 0):
                        self.direction = (-CELL_SIZE, 0)
                    if event.key == pygame.K_RIGHT and self.direction != (-CELL_SIZE, 0):
                        self.direction = (CELL_SIZE, 0)
                    if event.key == pygame.K_UP and self.direction != (0, CELL_SIZE):
                        self.direction = (0, -CELL_SIZE)
                    if event.key == pygame.K_DOWN and self.direction != (0, -CELL_SIZE):
                        self.direction = (0, CELL_SIZE)

            self.move()
            self.draw()

        return {
            "quit": False,
            "score": self.score,
            "level": self.level
        }