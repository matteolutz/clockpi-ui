from typing import Tuple

import pygame

from clockpi_ui.config import Config
from clockpi_ui.navigator import Navigator
from clockpi_ui.screen import Screen
from clockpi_ui.ui import Button, ButtonVariant
from clockpi_ui.ui.colors import PRIMARY, PRIMARY_BACKDROP


class SetAlarmScreen(Screen):
    def __init__(self) -> None:
        self._submit_button = Button(variant=ButtonVariant.DEFAULT, label="Ok")

        self._hour_up_button = Button(variant=ButtonVariant.DEFAULT, label="+")
        self._hour_down_button = Button(variant=ButtonVariant.DEFAULT, label="-")

        self._minute_up_button = Button(variant=ButtonVariant.DEFAULT, label="+")
        self._minute_down_button = Button(variant=ButtonVariant.DEFAULT, label="-")

        self._time_font = pygame.font.SysFont("Ubuntu", 48)

        self._alarm_time = Config.instance().get_alarm_time()

    def __render_hour(self, screen: pygame.Surface, center: Tuple[int, int]):
        text = self._time_font.render(f"{self._alarm_time['hour']:02d}", True, PRIMARY)
        screen.blit(
            text,
            (
                center[0] - text.get_width() // 2,
                center[1] - text.get_height() // 2,
            ),
        )

        button_size = (50, 50)
        self._hour_up_button.render_with_pos_and_size(
            screen,
            (center[0] - button_size[0] // 2, center[1] - button_size[1] - 30),
            button_size,
        )
        self._hour_down_button.render_with_pos_and_size(
            screen,
            (center[0] - button_size[0] // 2, center[1] + 30),
            button_size,
        )

    def __render_minute(self, screen: pygame.Surface, center: Tuple[int, int]):
        text = self._time_font.render(
            f"{self._alarm_time['minute']:02d}", True, PRIMARY
        )
        screen.blit(
            text,
            (
                center[0] - text.get_width() // 2,
                center[1] - text.get_height() // 2,
            ),
        )

        button_size = (50, 50)
        self._minute_up_button.render_with_pos_and_size(
            screen,
            (center[0] - button_size[0] // 2, center[1] - button_size[1] - 30),
            button_size,
        )
        self._minute_down_button.render_with_pos_and_size(
            screen,
            (center[0] - button_size[0] // 2, center[1] + 30),
            button_size,
        )

    def render(self, screen: pygame.Surface, dt: int):
        screen.fill(PRIMARY_BACKDROP)

        rect = screen.get_rect()
        rect.size = (int(rect.width * 0.8), int(rect.height * 0.8))
        rect.center = screen.get_rect().center

        self._submit_button.render_with_pos_and_size(
            screen, (rect.right - 80, rect.y + 10), (70, 50)
        )

        hour_center = (rect.centerx - rect.width // 8, rect.centery)
        self.__render_hour(screen, hour_center)

        minute_center = (rect.centerx + rect.width // 8, rect.centery)
        self.__render_minute(screen, minute_center)

        text = self._time_font.render(":", True, PRIMARY)
        screen.blit(
            text,
            (
                rect.centerx - text.get_width() // 2,
                rect.centery - text.get_height() // 2,
            ),
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
                self.submit()
                Navigator.instance().pop()
                return True

            if self._hour_up_button.was_clicked(event.pos):
                self._alarm_time["hour"] = (self._alarm_time["hour"] + 1) % 24
                return True

            if self._hour_down_button.was_clicked(event.pos):
                self._alarm_time["hour"] = (self._alarm_time["hour"] - 1) % 24
                return True

            if self._minute_up_button.was_clicked(event.pos):
                self._alarm_time["minute"] = (self._alarm_time["minute"] + 1) % 60
                return True

            if self._minute_down_button.was_clicked(event.pos):
                self._alarm_time["minute"] = (self._alarm_time["minute"] - 1) % 60
                return True

            # Prevent event propagation
            return True

        return False

    def surface_flags(self) -> int:
        return pygame.SRCALPHA

    def submit(self):
        Config.instance().set_alarm_time(
            self._alarm_time["hour"], self._alarm_time["minute"]
        )
