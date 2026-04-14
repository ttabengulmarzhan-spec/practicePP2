import pygame
import sys
import math
from clock import Clock

WIDTH, HEIGHT = 600, 650
FPS = 30
CENTER = (WIDTH // 2, 290)

WHITE     = (255, 255, 255)
BLACK     = (0, 0, 0)
CREAM     = (255, 248, 220)
RED       = (210, 30, 30)
DARK_GRAY = (40, 40, 40)
GOLD      = (218, 165, 32)
YELLOW    = (255, 220, 0)
L_GRAY    = (190, 190, 190)


SKIN = (240, 220, 200)


def draw_clock_face(surface, cx, cy, radius):
    pygame.draw.circle(surface, DARK_GRAY, (cx, cy), radius + 14)
    pygame.draw.circle(surface, CREAM, (cx, cy), radius)

    # hour marks
    for i in range(24):
        a = math.radians(i * 15)
        x1 = cx + int((radius - 18) * math.sin(a))
        y1 = cy - int((radius - 18) * math.cos(a))
        x2 = cx + int(radius * math.sin(a))
        y2 = cy - int(radius * math.cos(a))
        pygame.draw.line(surface, L_GRAY, (x1, y1), (x2, y2), 1)

    # numbers
    font = pygame.font.SysFont("Arial", 26, bold=True)
    for h in range(1, 13):
        a = math.radians(h * 30)
        nx = cx + int((radius - 42) * math.sin(a))
        ny = cy - int((radius - 42) * math.cos(a))
        label = font.render(str(h), True, DARK_GRAY)
        surface.blit(label, label.get_rect(center=(nx, ny)))

    # minute marks
    for i in range(60):
        a = math.radians(i * 6)
        thick = 3 if i % 5 == 0 else 1
        length = 14 if i % 5 == 0 else 6

        x1 = cx + int((radius - 2) * math.sin(a))
        y1 = cy - int((radius - 2) * math.cos(a))
        x2 = cx + int((radius - 2 - length) * math.sin(a))
        y2 = cy - int((radius - 2 - length) * math.cos(a))

        pygame.draw.line(surface, DARK_GRAY, (x1, y1), (x2, y2), thick)


def make_hand(length, shaft_w, color, glove_r):
    pad = 12
    sw = max(shaft_w + 10, glove_r * 2 + 6) + pad * 2
    sh = length + glove_r * 2 + pad * 2

    surf = pygame.Surface((sw, sh), pygame.SRCALPHA)

    cx = sw // 2
    top = pad + glove_r
    bottom = sh - pad

    bw = shaft_w // 2
    tw = max(2, shaft_w // 4)

    # hand body
    pygame.draw.polygon(surf, color, [
        (cx - bw, bottom),
        (cx + bw, bottom),
        (cx + tw, top + glove_r),
        (cx - tw, top + glove_r),
    ])

    # glove
    pygame.draw.circle(surf, WHITE, (cx, top), glove_r)
    pygame.draw.circle(surf, BLACK, (cx, top), glove_r, 2)

    # fingers
    r = max(2, glove_r // 3)
    for ox, oy in [(-r, -glove_r // 2), (0, -glove_r + 2), (r, -glove_r // 2)]:
        pygame.draw.circle(surf, WHITE, (cx + ox, top + oy), r)
        pygame.draw.circle(surf, BLACK, (cx + ox, top + oy), 1)

    return surf, (cx, bottom)


def blit_rotated(surface, img, pivot, angle, center):
    rotated = pygame.transform.rotate(img, -angle)

    rect = img.get_rect(
        topleft=(center[0] - pivot[0], center[1] - pivot[1])
    )

    offset = pygame.math.Vector2(center) - pygame.math.Vector2(rect.center)
    rotated_offset = offset.rotate(angle)
    new_center = pygame.math.Vector2(center) - rotated_offset

    new_rect = rotated.get_rect(center=new_center)
    surface.blit(rotated, new_rect)


def draw_mickey(surface, cx, cy):
    # ears
    pygame.draw.circle(surface, BLACK, (cx - 32, cy - 88), 23)
    pygame.draw.circle(surface, BLACK, (cx + 32, cy - 88), 23)

    # head
    pygame.draw.circle(surface, BLACK, (cx, cy - 62), 38)

    # face
    pygame.draw.ellipse(surface, SKIN, pygame.Rect(cx - 20, cy - 62, 40, 30))

    # eyes
    pygame.draw.circle(surface, WHITE, (cx - 14, cy - 72), 10)
    pygame.draw.circle(surface, WHITE, (cx + 14, cy - 72), 10)
    pygame.draw.circle(surface, BLACK, (cx - 13, cy - 72), 6)
    pygame.draw.circle(surface, BLACK, (cx + 13, cy - 72), 6)

    # nose
    pygame.draw.ellipse(surface, BLACK, pygame.Rect(cx - 8, cy - 58, 16, 10))

    # body (bigger)
    pygame.draw.ellipse(surface, BLACK, pygame.Rect(cx - 45, cy - 10, 90, 120))

    # red pants
    pygame.draw.ellipse(surface, RED, pygame.Rect(cx - 38, cy + 30, 76, 60))

    # buttons
    pygame.draw.circle(surface, GOLD, (cx - 12, cy + 40), 6)
    pygame.draw.circle(surface, GOLD, (cx + 12, cy + 40), 6)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey Clock")

    clock_obj = Clock()
    fps = pygame.time.Clock()

    RADIUS = 230

    minute_hand, minute_pivot = make_hand(170, 12, DARK_GRAY, 16)
    second_hand, second_pivot = make_hand(200, 5, RED, 10)

    font = pygame.font.SysFont("Arial", 28, bold=True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

        screen.fill(WHITE)

        draw_clock_face(screen, *CENTER, RADIUS)

        now = clock_obj.get_time()

        minute_angle = clock_obj.get_minute_angle(now)
        second_angle = clock_obj.get_second_angle(now)

        blit_rotated(screen, minute_hand, minute_pivot, minute_angle, CENTER)
        blit_rotated(screen, second_hand, second_pivot, second_angle, CENTER)

        draw_mickey(screen, CENTER[0], CENTER[1] + 40)

        pygame.draw.circle(screen, DARK_GRAY, CENTER, 10)
        pygame.draw.circle(screen, GOLD, CENTER, 6)

        time_text = font.render(now.strftime("%H:%M:%S"), True, DARK_GRAY)
        screen.blit(time_text, time_text.get_rect(center=(WIDTH // 2, HEIGHT - 30)))

        pygame.display.flip()
        fps.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()