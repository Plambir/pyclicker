import pygame
from pygame.locals import *

class Application:
    def __init__(self, screen_size, caption):
        pygame.init()
        self.display_surface = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(caption)
        self.is_run = False
        self.update_func = self.__update_stub
        self.draw_func = self.__draw_stub
        self.keyup_listeners = []
        self.keydown_listeners = []
        self.mouseup_listeners = []
        self.mousedown_listeners = []

    def __update_stub(self):
        pass

    def __draw_stub(self, display_surface):
        pass

    def set_update(self, update):
        self.update_func = update

    def set_draw(self, draw):
        self.draw_func = draw

    def esc(self):
        self.is_run = False

    def append_keyup_listener(self, listener):
        self.keyup_listeners.append(listener)

    def remove_keyup_listener(self, listener):
        self.keyup_listeners.remove(listener)

    def append_keydown_listener(self, listener):
        self.keydown_listeners.append(listener)

    def remove_keydown_listener(self, listener):
        self.keydown_listeners.remove(listener)

    def append_mouseup_listener(self, listener):
        self.mouseup_listeners.append(listener)

    def remove_mouseup_listener(self, listener):
        self.mouseup_listeners.remove(listener)

    def append_mousedown_listener(self, listener):
        self.mousedown_listeners.append(listener)

    def remove_mousedown_listener(self, listener):
        self.mousedown_listeners.remove(listener)

    def __events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.esc()
            elif event.type == KEYUP:
                for listener in self.keyup_listeners:
                    listener(event.type, event.key)
            elif event.type == KEYDOWN:
                for listener in self.keydown_listeners:
                    listener(event.type, event.key)
            elif event.type == MOUSEBUTTONUP:
                for listener in self.mouseup_listeners:
                    listener(event.type, event.button, event.pos)
            elif event.type == MOUSEBUTTONDOWN:
                for listener in self.mousedown_listeners:
                    listener(event.type, event.button, event.pos)

    def __update(self):
        self.update_func()

    def __draw(self):
        self.draw_func(self.display_surface)

    def run(self):
        self.is_run = True
        while self.is_run:
            self.__events()
            self.__update()
            self.__draw()
            pygame.display.update()
        pygame.quit()

