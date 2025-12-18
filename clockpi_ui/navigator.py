import pygame

from clockpi_ui.screen import Screen
from clockpi_ui.utils import Singleton


@Singleton
class Navigator:
    def __init__(self):
        self.screens: list[Screen] = []
        self.render_stack: list[Screen] = []

    def __build_render_stack(self):
        self.render_stack.clear()
        for s in self.screens:
            if not s.is_overlay():
                self.render_stack.clear()
            self.render_stack.append(s)

    def push(self, screen: Screen):
        self.screens.append(screen)
        self.__build_render_stack()

    def pop(self):
        self.screens.pop()
        self.__build_render_stack()

    def update(self, dt: int):
        for s in self.screens:
            s.update(dt)

    def render(self, screen: pygame.Surface, dt: int):
        if not self.render_stack:
            screen.fill((255, 0, 0))
            return

        for s in self.render_stack:
            s.render(screen, dt)
