import pygame

from clockpi_ui.navigator import Navigator
from clockpi_ui.screen import Screen
from clockpi_ui.ui import Button, ButtonVariant
from clockpi_ui.ui.colors import PRIMARY, PRIMARY_BACKDROP


class SetAlarmScreen(Screen):
    def __init__(self) -> None:
        self._submit_button = Button(variant=ButtonVariant.DEFAULT, label="Ok")

    def render(self, screen: pygame.Surface, dt: int):
        screen.fill(PRIMARY_BACKDROP)

        rect = screen.get_rect()
        rect.size = (int(rect.width * 0.8), int(rect.height * 0.8))
        rect.center = screen.get_rect().center

        self._submit_button.render_with_pos_and_size(
            screen, (rect.right - 60, rect.y + 10), (50, 30)
        )

        pygame.draw.rect(screen, PRIMARY, rect, 2)

    def is_overlay(self) -> bool:
        return True

    def handle_event(self, event: pygame.event.Event, screen: pygame.Surface) -> bool:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Navigator.instance().pop()
            return True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._submit_button.was_clicked(event.pos):
                Navigator.instance().pop()

            # Prevent event propagation
            return True

        return False

    def surface_flags(self) -> int:
        return pygame.SRCALPHA
