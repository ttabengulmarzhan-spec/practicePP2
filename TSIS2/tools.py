import math
from collections import deque
import pygame

def draw_shape(surface, tool, start, end, color, width):
    x1, y1 = start
    x2, y2 = end

    if tool == "line":
        pygame.draw.line(surface, color, start, end, width)

    elif tool == "rect":
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(surface, color, rect, width)

    elif tool == "circle":
        radius = int(math.hypot(x2 - x1, y2 - y1))
        pygame.draw.circle(surface, color, start, radius, width)

    elif tool == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))
        sx = x1 if x2 >= x1 else x1 - side
        sy = y1 if y2 >= y1 else y1 - side
        pygame.draw.rect(surface, color, pygame.Rect(sx, sy, side, side), width)

    elif tool == "right_triangle":
        points = [start, (x2, y1), (x1, y2)]
        pygame.draw.polygon(surface, color, points, width)

    elif tool == "equilateral_triangle":
        side = max(1, abs(x2 - x1))
        direction = -1 if y2 < y1 else 1
        height = int((math.sqrt(3) / 2) * side) * direction
        points = [
            (x1, y1),
            (x1 + side, y1),
            (x1 + side // 2, y1 + height),
        ]
        pygame.draw.polygon(surface, color, points, width)

    elif tool == "rhombus":
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        points = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
        pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface, start_pos, fill_color):
    w, h = surface.get_size()
    x, y = start_pos
    if x < 0 or x >= w or y < 0 or y >= h:
        return

    target_color = surface.get_at((x, y))
    replacement = pygame.Color(fill_color[0], fill_color[1], fill_color[2], 255)

    if target_color == replacement:
        return

    q = deque()
    q.append((x, y))

    while q:
        cx, cy = q.popleft()

        if cx < 0 or cx >= w or cy < 0 or cy >= h:
            continue
        if surface.get_at((cx, cy)) != target_color:
            continue

        surface.set_at((cx, cy), replacement)
        q.append((cx + 1, cy))
        q.append((cx - 1, cy))
        q.append((cx, cy + 1))
        q.append((cx, cy - 1))
