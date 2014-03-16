#!/usr/bin/env python2
# encoding: utf-8

import random
import game

import pygame
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

class GameRule:
    def __init__(self):
        self.current = self.start

    def start(self):
        pass

    def respawn(self):
        pass

    def wait_input(self):
        pass

    def game_over(self):
        pass

    def update(self):
        self.current()


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
        self.grid = game.Grid()
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

class GameApplication:
    def __init__(self):
        self.app = game.Application(SCREEN, "PyClicker")
        self.app.append_keyup_listener(self.keyup_esc)
        self.app.append_mouseup_listener(self.mouseup)
        self.app.set_update(self.update)
        self.app.set_draw(self.draw)
        self.app.set_fps_limit(30)
        self.game = GameView()
        self.game.grid.random(50)
        self.game.update()

    def update(self, dt):
        self.game.update()

    def draw(self, display_surface, dt):
        self.game.draw(display_surface)

    def keyup_esc(self, type, key):
        if key == K_ESCAPE:
            self.app.esc()

    def mouseup(self, type, button, pos):
        if button == 1:
            self.game.click(pos)

    def run(self):
        self.app.run()

if __name__ == '__main__':
    app = GameApplication()
    app.run()
