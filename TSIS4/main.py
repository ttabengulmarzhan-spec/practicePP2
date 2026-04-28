import json
import os
import sys
import pygame

from db import init_db, save_game_session, get_top10, get_personal_best
from game import SnakeGame, WIDTH, HEIGHT


SETTINGS_FILE = "settings.json"
MUSIC_FILE = "/Users/gulmarzantaben/Desktop/PracticePP2/TSIS4/assets/ILLIT  - Almond Chocolate.mp3"


pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 4 - Snake Extended")
clock = pygame.time.Clock()

title_font = pygame.font.SysFont("Verdana", 36, bold=True)
font = pygame.font.SysFont("Verdana", 22)
small = pygame.font.SysFont("Verdana", 18)


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, (40, 40, 40), self.rect, border_radius=8)
        pygame.draw.rect(surface, (220, 220, 220), self.rect, 2, border_radius=8)
        txt = font.render(self.text, True, (255, 255, 255))
        surface.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def load_settings():
    default = {"snake_color": [0, 200, 0], "grid": True, "sound": True}
    if not os.path.exists(SETTINGS_FILE):
        return default
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        default.update(data)
        return default
    except Exception:
        return default


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)


def apply_music(settings):
    if settings.get("sound", True):
        if os.path.exists(MUSIC_FILE):
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(MUSIC_FILE)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()


def draw_center(text, y, color=(255, 255, 255), fnt=font):
    txt = fnt.render(text, True, color)
    screen.blit(txt, txt.get_rect(center=(WIDTH // 2, y)))


def main():
    init_db()

    settings = load_settings()
    apply_music(settings)

    username = ""
    state = "menu"
    last_result = None
    last_pb = 0

    color_presets = [
        [0, 200, 0],
        [0, 140, 255],
        [255, 140, 0],
        [180, 60, 220],
        [220, 40, 40],
    ]
    color_idx = 0
    if settings["snake_color"] in color_presets:
        color_idx = color_presets.index(settings["snake_color"])

    while True:
        clock.tick(60)

        if state == "menu":
            play_btn = Button(210, 170, 180, 45, "Play")
            lb_btn = Button(210, 225, 180, 45, "Leaderboard")
            set_btn = Button(210, 280, 180, 45, "Settings")
            quit_btn = Button(210, 335, 180, 45, "Quit")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.unicode and event.unicode.isprintable() and len(username) < 16:
                        username += event.unicode

                if play_btn.clicked(event):
                    if username.strip():
                        last_pb = get_personal_best(username.strip())
                        game = SnakeGame(screen, settings, username.strip(), last_pb)
                        result = game.run()
                        if result.get("quit"):
                            pygame.quit()
                            sys.exit()
                        save_game_session(username.strip(), result["score"], result["level"])
                        last_result = result
                        last_pb = max(last_pb, result["score"])
                        state = "game_over"

                elif lb_btn.clicked(event):
                    state = "leaderboard"
                elif set_btn.clicked(event):
                    state = "settings"
                elif quit_btn.clicked(event):
                    pygame.quit()
                    sys.exit()

            apply_music(settings)

            screen.fill((30, 30, 50))
            draw_center("SNAKE EXTENDED", 70, fnt=title_font)
            draw_center("Enter username:", 120)

            input_box = pygame.Rect(170, 135, 260, 32)
            pygame.draw.rect(screen, (255, 255, 255), input_box)
            pygame.draw.rect(screen, (80, 80, 80), input_box, 2)
            txt = small.render(username + "|", True, (20, 20, 20))
            screen.blit(txt, (input_box.x + 8, input_box.y + 7))

            play_btn.draw(screen)
            lb_btn.draw(screen)
            set_btn.draw(screen)
            quit_btn.draw(screen)

            pygame.display.flip()

        elif state == "leaderboard":
            back_btn = Button(240, 350, 120, 40, "Back")
            rows = get_top10()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if back_btn.clicked(event):
                    state = "menu"

            screen.fill((20, 20, 25))
            draw_center("TOP 10 LEADERBOARD", 40, fnt=font)
            y = 80

            if not rows:
                draw_center("No results yet", 160, fnt=small)
            else:
                for i, row in enumerate(rows, start=1):
                    uname, score, lvl, played = row
                    line = f"{i}. {uname} | score {score} | lvl {lvl} | {played.strftime('%Y-%m-%d')}"
                    t = small.render(line, True, (230, 230, 230))
                    screen.blit(t, (35, y))
                    y += 28

            back_btn.draw(screen)
            pygame.display.flip()

        elif state == "settings":
            
            grid_btn = Button(190, 140, 220, 45, f"Grid: {'ON' if settings['grid'] else 'OFF'}")
            sound_btn = Button(190, 195, 220, 45, f"Sound: {'ON' if settings['sound'] else 'OFF'}")
            save_back_btn = Button(190, 320, 220, 45, "Save & Back")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if grid_btn.clicked(event):
                    settings["grid"] = not settings["grid"]

                elif sound_btn.clicked(event):
                    settings["sound"] = not settings["sound"]
                    apply_music(settings)

                elif save_back_btn.clicked(event):
                    save_settings(settings)
                    apply_music(settings)
                    state = "menu"

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    color_rect = pygame.Rect(190, 250, 220, 45)
                    if color_rect.collidepoint(event.pos):
                        color_idx = (color_idx + 1) % len(color_presets)
                        settings["snake_color"] = color_presets[color_idx]

            screen.fill((42, 28, 28))

            draw_center("SETTINGS", 70, fnt=title_font)

            grid_btn.draw(screen)
            sound_btn.draw(screen)
            save_back_btn.draw(screen)

            snake_color = tuple(settings["snake_color"])

            color_rect = pygame.Rect(190, 250, 220, 45)

            pygame.draw.rect(screen, snake_color, color_rect, border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255), color_rect, 2, border_radius=8)

            text = font.render("Snake Color", True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=color_rect.center))

            pygame.display.flip()


if __name__ == "__main__":
    main()

