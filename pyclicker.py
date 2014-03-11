#!/usr/bin/env python2
# encoding: utf-8

import pygame
import random
from pygame.locals import *

COLOR0 = (255, 255, 255)
COLOR1 = (178, 60,  60)
COLOR2 = (134, 105, 48)
COLOR3 = (162, 60,  138)
COLOR4 = (56,  125, 101)
COLOR5 = (77,  60,  174)

FIRST_CHIP = (40,  60)
CHIP_SIZE  = (40, 40)
WIDTH = 6
HEIGHT = 10

class Cell:
    def __init__(self, x, y):
        self.chip = None
        self.x = x
        self.y = y

    def set_chip(self, chip):
        self.chip = chip

    def get_color(self):
        if self.chip is None:
            return COLOR0
        else:
            return self.chip

    def random(self, luck, left, right, up, down):
        colors = [COLOR1, COLOR2, COLOR3, COLOR4, COLOR5]
        neighbords = [left, right, up, down]
        random.shuffle(neighbords)
        for neighbord in neighbords:
            if neighbord is None or neighbord.chip is None:
                continue
            if random.randint(1, 100) < luck:
                self.chip = neighbord.chip
                return
            if neighbord.chip in colors:
                colors.remove(neighbord.chip)
        random.shuffle(colors)
        self.chip = colors[0]


class Grid:
    def __init__(self):
        self.grid = [[Cell(x, y) for y in range(HEIGHT)] for x in range(WIDTH)]
        self.cells = []
        for x in range(WIDTH):
            for y in range(HEIGHT):
                self.cells.append(self.grid[x][y])

    def get(self, x, y):
        if x < 0 or x >= WIDTH:
            return None
        if y < 0 or y >= HEIGHT:
            return None
        return self.grid[x][y]

    def random(self, luck):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                left  = self.get(x - 1, y)
                right = self.get(x + 1, y)
                up    = self.get(x, y - 1)
                down  = self.get(x, y + 1)
                self.grid[x][y].random(luck, left, right, up, down)


class CellView(pygame.sprite.Sprite):
    def __init__(self, cell):
        pygame.sprite.Sprite.__init__(self)
        self.cell = cell
        self.update()
        self.rect = self.image.get_rect()
        x = cell.x * CHIP_SIZE[0] + FIRST_CHIP[0]
        y = cell.y * CHIP_SIZE[1] + FIRST_CHIP[1]
        self.rect.move_ip(x, y)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def update(self):
        #TODO: get ref not value
        self.image = pygame.Surface(CHIP_SIZE)
        self.image.fill(self.cell.get_color())

class GameView:
    def __init__(self):
        self.grid = Grid()
        self.cell_views = pygame.sprite.Group()
        for cell in self.grid.cells:
            self.cell_views.add(CellView(cell))

    def update(self):
        self.cell_views.update()

    def draw(self, surface):
        self.cell_views.draw(surface)

    def click(self, pos):
        for cell_view in self.cell_views:
            if cell_view.collidepoint(pos):
                cell_view.cell.set_chip(COLOR0)
                return

class Application:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((320,480))
        pygame.display.set_caption("PyClicker")
        self.is_run = False
        self.game = GameView()
        self.game.grid.random(50)
        self.game.update()

    def esc(self):
        self.is_run = False

    def run(self):
        self.is_run = True
        while self.is_run:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.esc()
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.esc()
                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        self.game.click(event.pos)
            self.game.update()
            self.game.draw(self.display_surface)
            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    app = Application()
    app.run()
