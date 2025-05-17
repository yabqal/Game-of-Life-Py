import pygame as pg
import numpy as np

WIDTH, HEIGHT = 800, 700
CELL_SIZE = 10
ROW = HEIGHT // CELL_SIZE
COLUMN = WIDTH // CELL_SIZE

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

grid = np.random.choice([0, 1], size=(ROW, COLUMN))

'''grid[5, 5] = 1
grid[6, 5] = 1
grid[7, 5] = 1
grid[7, 4] = 1
grid[6, 3] = 1'''


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

        # Font setup
        self.font = pg.font.SysFont(None, 24)
        self.text_surf = self.font.render(text, True, "#ffffff")
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        # Draw button with hover effect
        color = self.hover_color if self.is_hovered else self.color
        pg.draw.rect(surface, color, self.rect)
        surface.blit(self.text_surf, self.text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click


button = Button(300, 250, 200, 50, "Play", (0, 0, 255), (255, 0, 0))


def update(grid):
    new_grid = np.zeros_like(grid)
    for r in range(ROW):
        for c in range(COLUMN):
            neighbors = np.sum(grid[max(0, r - 1):min(ROW, r + 2), max(0, c - 1):min(COLUMN, c + 2)]) - grid[r, c]
            if grid[r, c] == 1 and neighbors in (2, 3):
                new_grid[r, c] = 1
            elif grid[r, c] == 0 and neighbors == 3:
                new_grid[r, c] = 1
    return new_grid


def draw(grid):
    screen.fill((0, 0, 0))
    for r in range(ROW):
        for c in range(COLUMN):
            if grid[r, c] == 1:
                pg.draw.rect(screen, (255, 255, 255), (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE - 1, CELL_SIZE - 1))
    button.draw(screen)
    pg.display.flip()


running = True
paused = False

while running:
    mouse_pos = pg.mouse.get_pos()
    mouse_click = False

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                paused = not paused
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_click = True

    button.check_hover(mouse_pos)
    if button.is_clicked(mouse_pos, mouse_click):
        paused = not paused

    if not paused:
        button = Button(360, 646, 80, 28, "Pause", "#444444", (255, 0, 0))
        grid = update(grid)
        draw(grid)
    else:
        button = Button(360, 646, 80, 28, "Play", "#444444", (255, 0, 0))
        button.draw(screen)
        pg.display.flip()
    clock.tick(10)
