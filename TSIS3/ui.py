import pygame

class Button:
    def __init__(self, x, y, w, h, text, bg=(40, 40, 40), fg=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.bg = bg
        self.fg = fg

    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)
        color = tuple(min(255, c + 25) for c in self.bg) if hovered else self.bg

        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (220, 220, 220), self.rect, 2, border_radius=10)

        txt = font.render(self.text, True, self.fg)
        txt_rect = txt.get_rect(center=self.rect.center)
        surface.blit(txt, txt_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_center_text(surface, text, font, color, y):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(surface.get_width() // 2, y))
    surface.blit(rendered, rect)
