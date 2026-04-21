import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    radius = 10
    color = (0, 0, 255)
    mode = 'draw'

    points = []
    start_pos = None

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

                elif event.key == pygame.K_1:
                    mode = 'rect'
                elif event.key == pygame.K_2:
                    mode = 'circle'
                elif event.key == pygame.K_3:
                    mode = 'eraser'
                elif event.key == pygame.K_0:
                    mode = 'draw'

            if event.type == pygame.MOUSEBUTTONDOWN:
                start_pos = event.pos

                if event.button == 1:
                    radius = min(50, radius + 1)
                elif event.button == 3:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEMOTION and event.buttons[0]:
                pos = event.pos

                if mode == 'eraser':
                    pygame.draw.circle(screen, (0, 0, 0), pos, radius)
                elif mode == 'draw':
                    points.append(pos)
                    if len(points) > 1:
                        pygame.draw.line(screen, color, points[-2], points[-1], radius)

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

                points = [] 

        pygame.display.flip()
        clock.tick(60)


main()