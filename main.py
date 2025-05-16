import pygame as pg
import numpy as np

WIDTH, HEIGHT = 800, 800
CELL_SIZE = 10
ROW = HEIGHT // CELL_SIZE
COLUMN = WIDTH // CELL_SIZE

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

grid = np.random.choice([0, 0], size=(ROW, COLUMN))

grid[5, 5] = 1
grid[6, 5] = 1
grid[7, 5] = 1
grid[7, 4] = 1
grid[6, 3] = 1


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
    pg.display.flip()


running = True
paused = False

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                paused = not paused

    if not paused:
        grid = update(grid)
    draw(grid)
    clock.tick(10)
