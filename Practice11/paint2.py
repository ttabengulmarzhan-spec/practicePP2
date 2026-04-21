import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 10
    color = (0, 0, 255)
    mode = 'draw'

    start_pos = None
    last_pos = None

    screen.fill((0, 0, 0))

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)

                elif event.key == pygame.K_0:
                    mode = 'draw'
                elif event.key == pygame.K_1:
                    mode = 'rect'
                elif event.key == pygame.K_2:
                    mode = 'circle'
                elif event.key == pygame.K_3:
                    mode = 'eraser'
                elif event.key == pygame.K_4:
                    mode = 'square'
                elif event.key == pygame.K_5:
                    mode = 'right_triangle'
                elif event.key == pygame.K_6:
                    mode = 'equilateral_triangle'
                elif event.key == pygame.K_7:
                    mode = 'rhombus'

            if event.type == pygame.MOUSEBUTTONDOWN:
                start_pos = event.pos
                last_pos = event.pos

                if event.button == 1:
                    radius = min(50, radius + 1)
                elif event.button == 3:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEMOTION and event.buttons[0]:
                pos = event.pos

                if mode == 'eraser':
                    pygame.draw.circle(screen, (0, 0, 0), pos, radius)

                elif mode == 'draw':
                    if last_pos:
                        pygame.draw.line(screen, color, last_pos, pos, radius)
                    last_pos = pos

            if event.type == pygame.MOUSEBUTTONUP:
                end_pos = event.pos

                if mode == 'rect' and start_pos:
                    rect = pygame.Rect(start_pos,
                        (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                    pygame.draw.rect(screen, color, rect, 2)

                elif mode == 'circle' and start_pos:
                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    r = int((dx**2 + dy**2) ** 0.5)
                    pygame.draw.circle(screen, color, start_pos, r, 2)

                elif mode == 'square' and start_pos:
                    size = min(abs(end_pos[0] - start_pos[0]),
                               abs(end_pos[1] - start_pos[1]))
                    pygame.draw.rect(screen, color,
                        pygame.Rect(start_pos[0], start_pos[1], size, size), 2)

                elif mode == 'right_triangle' and start_pos:
                    pygame.draw.polygon(screen, color, [
                        start_pos,
                        (end_pos[0], start_pos[1]),
                        (start_pos[0], end_pos[1])
                    ], 2)

                elif mode == 'equilateral_triangle' and start_pos:
                    side = abs(end_pos[0] - start_pos[0])
                    pts = [
                        start_pos,
                        (start_pos[0] + side, start_pos[1]),
                        (start_pos[0] + side // 2,
                         start_pos[1] - int((math.sqrt(3) / 2) * side))
                    ]
                    pygame.draw.polygon(screen, color, pts, 2)

                elif mode == 'rhombus' and start_pos:
                    mid_x = (start_pos[0] + end_pos[0]) // 2
                    mid_y = (start_pos[1] + end_pos[1]) // 2

                    pts = [
                        (mid_x, start_pos[1]),
                        (end_pos[0], mid_y),
                        (mid_x, end_pos[1]),
                        (start_pos[0], mid_y)
                    ]
                    pygame.draw.polygon(screen, color, pts, 2)

                start_pos = None
                last_pos = None

        pygame.display.flip()
        clock.tick(60)


main()