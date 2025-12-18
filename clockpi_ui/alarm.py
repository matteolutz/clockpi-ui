import logging
from datetime import datetime

import pygame
import serial

from clockpi_ui.config import Config
from clockpi_ui.utils import Singleton
from clockpi_ui.utils.paths import ASSETS_DIR

logger = logging.getLogger(__name__)


@Singleton
class Alarm:
    def __init__(self):
        self._ringing = False
        self._sound = pygame.mixer.Sound(ASSETS_DIR / "sounds" / "alarm.wav")
        self._serial = None

    def init_serial(self, serial_port: str):
        self._serial = serial.Serial(serial_port, baudrate=115200)

    def update(self):
        if not Config.instance().get_alarm_enabled():
            return

        alarm_datetime = Config.instance().next_alarm_datetime()
        now = datetime.now()

        if alarm_datetime <= now:
            self.ring()
            Config.instance().update_alarm_next_datetime()

    def ring(self):
        if self._ringing:
            return
        logger.info("Alarm ringing")
        self._sound.play(loops=-1)

        if self._serial:
            # Command = 0x1, Speed = 0x1
            self._serial.write(bytes([0x01, 0x01]))
        self._ringing = True

    def stop(self):
        if not self._ringing:
            return
        logger.info("Alarm stopped")
        self._sound.stop()

        if self._serial:
            # Command = 0x1, Speed = 0xFF (-1)
            self._serial.write(bytes([0x01, 0xFF]))

        self._ringing = False

    def is_ringing(self):
        return self._ringing
