import logging

import pygame

from clockpi_ui.alarm import Alarm
from clockpi_ui.navigator import Navigator
from clockpi_ui.screens import ClockScreen

from .config import Config

RESOLUTION = (480, 320)
FULLSCREEN = False

logger = logging.getLogger(__name__)


def init_pygame():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()


def handle_pygame_event(event: pygame.event.Event) -> bool:
    if event.type == pygame.QUIT:
        return True

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            return True

        if event.key == pygame.K_SPACE:
            if Alarm.instance().is_ringing():
                Alarm.instance().stop()
            else:
                Config.instance().toggle_alarm_enabled()

    return False


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Starting ClockPi UI")

    Config.instance().load_config()

    init_pygame()
    screen = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN if FULLSCREEN else 0)
    clock = pygame.time.Clock()
    running = True

    Navigator.instance().push(ClockScreen())

    while running:
        for event in pygame.event.get():
            if handle_pygame_event(event):
                running = False

        dt = clock.get_rawtime()

        Alarm.instance().update()

        Navigator.instance().update(dt)
        Navigator.instance().render(screen, dt)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    Config.instance().save_config()
