from datetime import datetime

import pygame
import pygame.freetype

from clockpi_ui.alarm import Alarm
from clockpi_ui.config import Config
from clockpi_ui.screen import Screen
from clockpi_ui.utils.paths import ASSETS_DIR


class ClockScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
        self._current_time_font = pygame.freetype.Font(
            ASSETS_DIR / "fonts" / "software_tester_7.ttf", 140
        )

        self._alarm_time_font = pygame.freetype.Font(
            ASSETS_DIR / "fonts" / "software_tester_7.ttf", 25
        )
        self._alarm_icon = pygame.transform.scale(
            pygame.image.load(ASSETS_DIR / "icons" / "alarm.png"), (25, 25)
        )

    def __render_current_time(self, screen: pygame.Surface):
        now = datetime.now()

        even_second = now.second % 2 == 0
        center_glyph = " " if even_second else ":"

        screen.fill((0, 0, 0))
        text_surface, text_rect = self._current_time_font.render(
            f"{str(now.hour).rjust(2, '0')}{center_glyph}{str(now.minute).rjust(2, '0')}",
            (255, 0, 0) if Alarm.instance().is_ringing() else (255, 255, 255),
        )

        text_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
        screen.blit(text_surface, text_rect)

    def __render_alarm_time(self, screen: pygame.Surface):
        alarm_time = Config.instance().get_alarm_time()
        alarm_enabled = Config.instance().get_alarm_enabled()

        alarm_icon_rect = self._alarm_icon.get_rect()
        alarm_icon_rect.bottomleft = (10, screen.get_height() - 10)

        screen.blit(self._alarm_icon, alarm_icon_rect)

        text_surface, text_rect = self._alarm_time_font.render(
            f"{str(alarm_time['hour']).rjust(2, '0')}:{str(alarm_time['minute']).rjust(2, '0')}",
            (255, 255, 255) if alarm_enabled else (100, 100, 100),
        )
        text_rect.left = alarm_icon_rect.right + 10
        text_rect.centery = alarm_icon_rect.centery
        screen.blit(text_surface, text_rect)

    def render(self, screen, dt):
        self.__render_current_time(screen)
        self.__render_alarm_time(screen)

    def is_overlay(self) -> bool:
        return False
