import random
import pygame

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_W = WIDTH // CELL_SIZE
GRID_H = HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (210, 40, 40)
DARK_RED = (130, 20, 20)
BLUE = (70, 120, 255)
ORANGE = (255, 165, 0)
PURPLE = (170, 80, 220)
GRAY = (220, 220, 220)


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
        self.poison_food = None
        self.powerup = None

        self.food = self.generate_food(weighted=True)
        self.food_spawn_time = pygame.time.get_ticks()
        self.food_lifetime = 4000

        self.poison_food = self.generate_food(weighted=False)
        self.poison_spawn_time = pygame.time.get_ticks()
        self.poison_lifetime = 6000

        self.powerup_spawn_time = 0
        self.powerup_lifetime = 8000
        self.last_powerup_attempt = pygame.time.get_ticks()


        self.running = True
        self.game_over = False

    def current_speed(self):
        speed = self.base_speed + (self.level - 1) * 2
        now = pygame.time.get_ticks()
        if self.speed_effect and now < self.speed_effect_end:
            if self.speed_effect == "boost":
                speed += 4
            elif self.speed_effect == "slow":
                speed = max(3, speed - 3)
        return speed

    def level_up_if_needed(self):
        if self.foods_eaten > 0 and self.foods_eaten % 3 == 0:
            self.level += 1
            if self.level >= 3:
                self.generate_obstacles_for_level()

    def grid_pos_to_px(self, gx, gy):
        return gx * CELL_SIZE, gy * CELL_SIZE

    def px_to_grid(self, x, y):
        return x // CELL_SIZE, y // CELL_SIZE

    def occupied_cells(self):
        cells = {self.px_to_grid(x, y) for x, y in self.snake}
        cells |= self.obstacles
        if self.food:
            cells.add(self.px_to_grid(self.food[0], self.food[1]))
        if self.poison_food:
            cells.add(self.px_to_grid(self.poison_food[0], self.poison_food[1]))
        if self.powerup:
            cells.add(self.px_to_grid(self.powerup["x"], self.powerup["y"]))
        return cells

    def random_free_cell(self):
        taken = self.occupied_cells()
        while True:
            gx = random.randint(0, GRID_W - 1)
            gy = random.randint(0, GRID_H - 1)
            if (gx, gy) not in taken:
                return gx, gy

    def generate_food(self, weighted=True):
        gx, gy = self.random_free_cell()
        x, y = self.grid_pos_to_px(gx, gy)
        if weighted:
            return (x, y, random.choice([1, 2, 3]))
        return (x, y)

    def generate_obstacles_for_level(self):
        head_g = self.px_to_grid(*self.snake[0])
        safe_zone = set()
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                sx = head_g[0] + dx
                sy = head_g[1] + dy
                if 0 <= sx < GRID_W and 0 <= sy < GRID_H:
                    safe_zone.add((sx, sy))

        count = min(5 + self.level * 2, 30)
        new_blocks = set()
        snake_cells = {self.px_to_grid(x, y) for x, y in self.snake}

        tries = 0
        while len(new_blocks) < count and tries < 4000:
            tries += 1
            gx = random.randint(0, GRID_W - 1)
            gy = random.randint(0, GRID_H - 1)

            if (gx, gy) in safe_zone:
                continue
            if (gx, gy) in snake_cells:
                continue
            if self.food and (gx, gy) == self.px_to_grid(self.food[0], self.food[1]):
                continue
            if self.poison_food and (gx, gy) == self.px_to_grid(self.poison_food[0], self.poison_food[1]):
                continue

            new_blocks.add((gx, gy))

        head_neighbors = [
            (head_g[0] + 1, head_g[1]),
            (head_g[0] - 1, head_g[1]),
            (head_g[0], head_g[1] + 1),
            (head_g[0], head_g[1] - 1),
        ]
        free_neighbors = 0
        for nx, ny in head_neighbors:
            if 0 <= nx < GRID_W and 0 <= ny < GRID_H and (nx, ny) not in new_blocks:
                free_neighbors += 1

        if free_neighbors >= 2:
            self.obstacles = new_blocks

    def spawn_powerup_if_needed(self):
        now = pygame.time.get_ticks()

        if self.powerup and now - self.powerup_spawn_time > self.powerup_lifetime:
            self.powerup = None

        active_timed = self.speed_effect and now < self.speed_effect_end
        if self.shield or active_timed:
            return

        if self.powerup is None and now - self.last_powerup_attempt > 3500:
            self.last_powerup_attempt = now
            gx, gy = self.random_free_cell()
            x, y = self.grid_pos_to_px(gx, gy)
            ptype = random.choice(["boost", "slow", "shield"])
            self.powerup = {"type": ptype, "x": x, "y": y}
            self.powerup_spawn_time = now

    def move_snake(self):
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        prev_head = self.snake[0]
        new_head = (head_x + dx, head_y + dy)

        self.snake.insert(0, new_head)
        self.snake.pop()

        if self.check_collision():
            if self.shield:
                self.shield = False
                self.snake[0] = prev_head
                return
            self.game_over = True
            self.running = False
            return

        if new_head == (self.food[0], self.food[1]):
            self.snake.append(self.snake[-1])
            self.score += self.food[2]
            self.foods_eaten += 1
            self.food = self.generate_food(weighted=True)
            self.food_spawn_time = pygame.time.get_ticks()
            self.level_up_if_needed()

        if new_head == self.poison_food:
            if len(self.snake) <= 3:
                self.game_over = True
                self.running = False
                return
            self.snake.pop()
            self.snake.pop()
            if len(self.snake) <= 1:
                self.game_over = True
                self.running = False
                return
            self.poison_food = self.generate_food(weighted=False)
            self.poison_spawn_time = pygame.time.get_ticks()

        if self.powerup and new_head == (self.powerup["x"], self.powerup["y"]):
            now = pygame.time.get_ticks()
            ptype = self.powerup["type"]
            if ptype == "boost":
                self.speed_effect = "boost"
                self.speed_effect_end = now + 5000
            elif ptype == "slow":
                self.speed_effect = "slow"
                self.speed_effect_end = now + 5000
            else:
                self.shield = True
                self.speed_effect = None
                self.speed_effect_end = 0
            self.powerup = None

    def check_collision(self):
        head_x, head_y = self.snake[0]

        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return True

        if self.snake[0] in self.snake[1:]:
            return True

        if self.px_to_grid(head_x, head_y) in self.obstacles:
            return True

        return False

    def update_items_timers(self):
        now = pygame.time.get_ticks()

        if now - self.food_spawn_time > self.food_lifetime:
            self.food = self.generate_food(weighted=True)
            self.food_spawn_time = now

        if now - self.poison_spawn_time > self.poison_lifetime:
            self.poison_food = self.generate_food(weighted=False)
            self.poison_spawn_time = now

        if self.speed_effect and now >= self.speed_effect_end:
            self.speed_effect = None
            self.speed_effect_end = 0

        self.spawn_powerup_if_needed()

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
            x, y = self.grid_pos_to_px(gx, gy)
            pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))

        pygame.draw.rect(self.screen, RED, (self.food[0], self.food[1], CELL_SIZE, CELL_SIZE))
        wtxt = self.font.render(str(self.food[2]), True, WHITE)
        self.screen.blit(wtxt, (self.food[0] + 5, self.food[1] + 1))

        pygame.draw.rect(self.screen, DARK_RED, (self.poison_food[0], self.poison_food[1], CELL_SIZE, CELL_SIZE))

        if self.powerup:
            color = BLUE if self.powerup["type"] == "boost" else ORANGE if self.powerup["type"] == "slow" else PURPLE
            pygame.draw.rect(self.screen, color, (self.powerup["x"], self.powerup["y"], CELL_SIZE, CELL_SIZE))

        snake_color = tuple(self.settings.get("snake_color", [0, 200, 0]))
        for i, block in enumerate(self.snake):
            clr = snake_color if i > 0 else (max(0, snake_color[0] - 30), max(0, snake_color[1] - 30), max(0, snake_color[2] - 30))
            pygame.draw.rect(self.screen, clr, (*block, CELL_SIZE, CELL_SIZE))

        now = pygame.time.get_ticks()
        effect_text = "None"
        if self.shield:
            effect_text = "Shield"
        elif self.speed_effect:
            left = max(0, (self.speed_effect_end - now) // 1000)
            effect_text = f"{self.speed_effect} {left}s"

        text = self.font.render(
            f"User: {self.username}  Score: {self.score}  Level: {self.level}  PB: {self.personal_best}  Power: {effect_text}",
            True,
            BLACK,
        )
        self.screen.blit(text, (8, 8))

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
                    elif event.key == pygame.K_RIGHT and self.direction != (-CELL_SIZE, 0):
                        self.direction = (CELL_SIZE, 0)
                    elif event.key == pygame.K_UP and self.direction != (0, CELL_SIZE):
                        self.direction = (0, -CELL_SIZE)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -CELL_SIZE):
                        self.direction = (0, CELL_SIZE)

            self.move_snake()
            self.update_items_timers()
            self.draw()

        return {
            "quit": False,
            "score": self.score,
            "level": self.level,
        }
