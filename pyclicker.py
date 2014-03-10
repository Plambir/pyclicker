#!/usr/bin/env python2
# encoding: utf-8

import pygame
from pygame.locals import *

pygame.init()
pygame.display.set_mode((320, 480))
pygame.display.set_caption("PyClicker")

run = True
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
    pygame.display.update()

pygame.quit()
