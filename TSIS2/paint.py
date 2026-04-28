import pygame
from datetime import datetime
from tools import draw_shape, flood_fill

WIDTH, HEIGHT = 1000, 700
TOOLBAR_H = 90
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (230, 50, 50)
GREEN = (40, 180, 80)
BLUE = (50, 90, 220)
GRAY = (235, 235, 235)
DARK = (35, 35, 35)


def clamp(value, low, high):
    return max(low, min(high, value))


def in_canvas(pos):
    return pos[1] >= TOOLBAR_H


def to_canvas_pos(pos):
    x = clamp(pos[0], 0, WIDTH - 1)
    y = clamp(pos[1] - TOOLBAR_H, 0, HEIGHT - TOOLBAR_H - 1)
    return x, y


def save_canvas(canvas):
    filename = f"paint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    pygame.image.save(canvas, filename)
    return filename


def draw_toolbar(screen, font, small_font, tool, color, brush_name, brush_px, msg):
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_H))
    pygame.draw.line(screen, DARK, (0, TOOLBAR_H - 1), (WIDTH, TOOLBAR_H - 1), 2)

    tool_text = (
        f"Tool: {tool} | Brush: {brush_name} ({brush_px}px) | "
        "Tools: P-pencil L-line E-eraser R-rect C-circle Q-square T-right Y-equilateral H-rhombus F-fill X-text"
    )
    ctrl_text = "Colors: K-black R-red G-green B-blue | Size: 1/2/3 | Ctrl+S save | Esc exit/cancel text"

    screen.blit(font.render(tool_text, True, DARK), (10, 10))
    screen.blit(small_font.render(ctrl_text, True, DARK), (10, 40))

    colors = [BLACK, RED, GREEN, BLUE, WHITE]
    x0 = 10
    for c in colors:
        pygame.draw.rect(screen, c, (x0, 62, 28, 20))
        if c == color:
            pygame.draw.rect(screen, (255, 165, 0), (x0 - 2, 60, 32, 24), 2)
        else:
            pygame.draw.rect(screen, DARK, (x0, 62, 28, 20), 1)
        x0 += 36

    if msg:
        screen.blit(small_font.render(msg, True, (20, 120, 20)), (WIDTH - 360, 64))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS 2 Paint - Extended")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("arial", 18)
    small_font = pygame.font.SysFont("arial", 15)

    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
    canvas.fill(WHITE)

    brush_sizes = {"small": 2, "medium": 5, "large": 10}
    brush_name = "medium"

    color = BLACK
    tool = "pencil"

    drawing = False
    start_pos = None
    current_pos = None
    last_pos = None

    text_active = False
    text_pos = None
    text_buffer = ""

    save_message = ""
    save_msg_until = 0

    preview_tools = {
        "line",
        "rect",
        "circle",
        "square",
        "right_triangle",
        "equilateral_triangle",
        "rhombus",
    }

    running = True
    while running:
        now_ms = pygame.time.get_ticks()
        if now_ms > save_msg_until:
            save_message = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if text_active:
                    if event.key == pygame.K_RETURN:
                        if text_buffer:
                            txt = font.render(text_buffer, True, color)
                            canvas.blit(txt, text_pos)
                        text_active = False
                        text_buffer = ""
                        text_pos = None
                    elif event.key == pygame.K_ESCAPE:
                        text_active = False
                        text_buffer = ""
                        text_pos = None
                    elif event.key == pygame.K_BACKSPACE:
                        text_buffer = text_buffer[:-1]
                    else:
                        if event.unicode and event.unicode.isprintable():
                            text_buffer += event.unicode
                    continue

                if event.key == pygame.K_ESCAPE:
                    running = False

                mods = pygame.key.get_mods()
                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    filename = save_canvas(canvas)
                    save_message = f"Saved: {filename}"
                    save_msg_until = now_ms + 2500

                if event.key == pygame.K_1:
                    brush_name = "small"
                elif event.key == pygame.K_2:
                    brush_name = "medium"
                elif event.key == pygame.K_3:
                    brush_name = "large"

                elif event.key == pygame.K_p:
                    tool = "pencil"
                elif event.key == pygame.K_l:
                    tool = "line"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_r:
                    tool = "rect"
                    color = RED
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_q:
                    tool = "square"
                elif event.key == pygame.K_t:
                    tool = "right_triangle"
                elif event.key == pygame.K_y:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_h:
                    tool = "rhombus"
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_x:
                    tool = "text"

                if event.key == pygame.K_k:
                    color = BLACK
                elif event.key == pygame.K_g:
                    color = GREEN
                elif event.key == pygame.K_b:
                    color = BLUE

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not in_canvas(event.pos):
                    continue

                pos = to_canvas_pos(event.pos)

                if tool == "fill":
                    flood_fill(canvas, pos, color)

                elif tool == "text":
                    text_active = True
                    text_pos = pos
                    text_buffer = ""

                else:
                    drawing = True
                    start_pos = pos
                    current_pos = pos
                    last_pos = pos

                    if tool == "pencil":
                        pygame.draw.circle(canvas, color, pos, max(1, brush_sizes[brush_name] // 2))
                    elif tool == "eraser":
                        pygame.draw.circle(canvas, WHITE, pos, max(1, brush_sizes[brush_name] // 2))

            elif event.type == pygame.MOUSEMOTION and drawing:
                if not in_canvas(event.pos):
                    pos = to_canvas_pos((event.pos[0], TOOLBAR_H))
                else:
                    pos = to_canvas_pos(event.pos)

                current_pos = pos
                stroke = brush_sizes[brush_name]

                if tool == "pencil":
                    pygame.draw.line(canvas, color, last_pos, pos, stroke)
                    last_pos = pos
                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, pos, stroke)
                    last_pos = pos

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
                end_pos = to_canvas_pos(event.pos)
                stroke = brush_sizes[brush_name]

                if tool in preview_tools and start_pos:
                    draw_shape(canvas, tool, start_pos, end_pos, color, stroke)

                drawing = False
                start_pos = None
                current_pos = None
                last_pos = None

        screen.fill((210, 210, 210))
        draw_toolbar(
            screen,
            font,
            small_font,
            tool,
            color,
            brush_name,
            brush_sizes[brush_name],
            save_message,
        )

        if drawing and tool in preview_tools and start_pos and current_pos:
            temp = canvas.copy()
            draw_shape(temp, tool, start_pos, current_pos, color, brush_sizes[brush_name])
            screen.blit(temp, (0, TOOLBAR_H))
        else:
            screen.blit(canvas, (0, TOOLBAR_H))

        if text_active and text_pos is not None:
            preview = font.render(text_buffer + "|", True, color)
            screen.blit(preview, (text_pos[0], text_pos[1] + TOOLBAR_H))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
