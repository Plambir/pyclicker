#!/usr/bin/env python2
# encoding: utf-8

import pygame
import random
from pygame.locals import *

SCREEN = (320, 480)
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

def swap_cell(cell_a, cell_b):
    chip_a = cell_a.chip
    cell_a.chip = cell_b.chip
    cell_b.chip = chip_a

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

    def random(self, luck, neighbors):
        colors = [COLOR1, COLOR2, COLOR3, COLOR4, COLOR5]
        random.shuffle(neighbors)
        for neighbor in neighbors:
            if neighbor is None or neighbor.chip is None:
                continue
            if random.randint(1, 100) < luck:
                self.chip = neighbor.chip
                return
            if neighbor.chip in colors:
                colors.remove(neighbor.chip)
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

    def get_neighbors(self, cell):
        return [
            self.get(cell.x - 1, cell.y),
            self.get(cell.x + 1, cell.y),
            self.get(cell.x, cell.y - 1),
            self.get(cell.x, cell.y + 1)
        ]

    def random(self, luck):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                neighbors = self.get_neighbors(self.grid[x][y])
                self.grid[x][y].random(luck, neighbors)

    def has_move(self):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if self.grid[x][y].chip is None:
                    continue
                neighbors = self.get_neighbors(self.grid[x][y])
                for neighbor in neighbors:
                    if neighbor is not None \
                        and neighbor.chip == self.grid[x][y].chip:
                        return True
        return False

    def is_pair(self, cell):
        color = cell.get_color()
        x = cell.x
        y = cell.y
        neighbors = self.get_neighbors(cell)
        for neighbor in neighbors:
            if neighbor is not None and neighbor.get_color() == color:
                return True
        return False

    def destroy(self, cell, score=1):
        color = cell.get_color()
        if cell.chip is None:
            return 0
        cell.set_chip(None)
        x = cell.x
        y = cell.y
        neighbors = self.get_neighbors(cell)
        for neighbor in neighbors:
            if neighbor is not None and neighbor.get_color() == color:
                score += self.destroy(neighbor, score)

        return score

    def fall(self, view):
        for y in reversed(range(HEIGHT)):
            for x in range(WIDTH):
                if self.grid[x][y].get_color() == COLOR0:
                    for up in reversed(range(y)):
                        if self.grid[x][up].get_color() != COLOR0:
                            swap_cell(self.grid[x][y], self.grid[x][up])
                            break

    def respawn(self, luck, view):
        self.fall(view)
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if self.grid[x][y].get_color() != COLOR0:
                    continue
                self.grid[x][y].random(luck, self.get_neighbors(self.grid[x][y]))



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
        self.font = pygame.font.SysFont("Arial", 12);
        for cell in self.grid.cells:
            self.cell_views.add(CellView(cell))
        self.score = 0
        self.move = 30
        self.game_over = False

    def update(self):
        if not self.grid.has_move():
            self.game_over = True
        self.cell_views.update()

    def draw(self, surface):
        surface.fill((0,0,0))
        if self.game_over:
            game_over_text = self.font.render("Game Over", 1, (255,255,255))
            rect = game_over_text.get_rect()
            rect.move(SCREEN[0] / 2 + rect.width / 2, SCREEN[1] / 2 + rect.height)
            surface.blit(game_over_text, rect)
        else:
            score_view = self.font.render("score: " + str(self.score), 1, (255,255,255))
            surface.blit(score_view, score_view.get_rect())
            move_text = "move: "
            if self.move < 0:
                move_text += str(0)
            else:
                move_text += str(self.move)
            move_view = self.font.render(move_text, 1, (255,255,255))
            surface.blit(move_view, score_view.get_rect().move(0, score_view.get_rect().height))
            self.cell_views.draw(surface)

    def click(self, pos):
        for cell_view in self.cell_views:
            if cell_view.collidepoint(pos):
                if self.grid.is_pair(cell_view.cell):
                    self.score += self.grid.destroy(cell_view.cell) * 2
                    self.move -= 1
                break
        self.grid.fall(self)
        if self.move >= 0:
            self.grid.respawn(30, self)

class Application:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode(SCREEN)
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
