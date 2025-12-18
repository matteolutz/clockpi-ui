import logging
import time

import pygame

from clockpi_ui.alarm import Alarm
from clockpi_ui.args import get_arg_parser
from clockpi_ui.navigator import Navigator
from clockpi_ui.screens import ClockScreen

from .config import Config

RESOLUTION = (480, 320)
FPS = 30

AUTOSAVE_INTERVAL = 30

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

    init_pygame()

    parser = get_arg_parser()
    args = parser.parse_args()

    if args.serial:
        logger.info(f"LED Serial Port: {args.serial}")
        Alarm.instance().init_serial(args.serial)

    Config.instance().load_config()
    last_autosave = time.time()

    screen = pygame.display.set_mode(
        RESOLUTION, pygame.FULLSCREEN if args.fullscreen else 0
    )
    clock = pygame.time.Clock()
    running = True

    Navigator.instance().push(ClockScreen())

    while running:
        for event in pygame.event.get():
            if Navigator.instance().handle_event(event, screen):
                continue
            if handle_pygame_event(event):
                running = False

        if time.time() - last_autosave > AUTOSAVE_INTERVAL:
            logger.info("Autosaving config")
            Config.instance().save_config()
            last_autosave = time.time()

        dt = clock.get_rawtime()

        Alarm.instance().update()

        Navigator.instance().update(dt)
        Navigator.instance().render(screen, dt)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    Config.instance().save_config()
