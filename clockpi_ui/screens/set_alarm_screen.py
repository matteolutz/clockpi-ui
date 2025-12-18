import pygame

from clockpi_ui.navigator import Navigator
from clockpi_ui.screen import Screen


class SetAlarmScreen(Screen):
    def __init__(self) -> None:
        pass

    def render(self, screen: pygame.Surface, dt: int):
        screen.fill((2, 0, 10, 240))

        rect = screen.get_rect()
        rect.size = (int(rect.width * 0.8), int(rect.height * 0.8))
        rect.center = screen.get_rect().center

        pygame.draw.rect(screen, (150, 0, 255), rect, 2)

    def is_overlay(self) -> bool:
        return True

    def handle_event(self, event: pygame.event.Event, screen: pygame.Surface) -> bool:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Navigator.instance().pop()
            return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Prevent event propagation
            return True

        return False

    def surface_flags(self) -> int:
        return pygame.SRCALPHA
