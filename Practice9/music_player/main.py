import pygame
import sys
import os
from player import MusicPlayer

# init
pygame.init()
pygame.mixer.init()

# window
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 28)
clock = pygame.time.Clock()

# player
player = MusicPlayer()

# helper for text
def draw_text(text, x, y):
    render = font.render(text, True, (255, 255, 255))
    screen.blit(render, (x, y))


running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()

            elif event.key == pygame.K_s:
                player.stop()

            elif event.key == pygame.K_n:
                player.next()

            elif event.key == pygame.K_b:
                player.prev()

            elif event.key == pygame.K_q:
                running = False

    # UI
    draw_text("🎵 MUSIC PLAYER", 20, 20)
    draw_text(f"Track: {os.path.basename(player.get_current_track())}", 20, 120)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()