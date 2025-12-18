import datetime
import logging

import yaml

from .utils import Singleton
from .utils.paths import CONFIG_FILE

logger = logging.getLogger(__name__)

CONFIG_DEFAULTS = {"alarm_time": {"hour": 0, "minute": 0}, "alarm_enabled": False}


@Singleton
class Config:
    def __init__(self) -> None:
        self._config = CONFIG_DEFAULTS
        self.update_alarm_next_datetime()

    def update_alarm_next_datetime(self):
        alarm_time = self.get_alarm_time()
        now = datetime.datetime.now()
        alarm = now.replace(
            hour=alarm_time["hour"],
            minute=alarm_time["minute"],
            second=0,
            microsecond=0,
        )

        if alarm < now:
            alarm += datetime.timedelta(days=1)

        logger.debug(f"Next alarm ringing in {alarm - now}")

        self._next_alarm_datetime = alarm

    def __create_config_dir(self):
        # Create config directory if it doesn't exist
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

    def __read_config_file(self):
        self.__create_config_dir()
        # Open config file and create if it doesn't exist
        # By using a+ the file is created if it doesn't exist but not truncated
        # By calling seek(0) to ensure we're at the beginning of the file
        f = open(CONFIG_FILE, "a+", encoding="utf-8")
        f.seek(0)
        return f

    def __write_config_file(self):
        self.__create_config_dir()
        # Open config file and create if it doesn't exist
        return open(CONFIG_FILE, "w", encoding="utf-8")

    def load_config(self):
        config_file = self.__read_config_file()
        logger.info(f'Loading config from "{config_file.name}"')

        self._config = yaml.safe_load(config_file)
        if self._config is None:
            self._config = CONFIG_DEFAULTS

        self.update_alarm_next_datetime()

        logger.debug(f"Config: {self._config}")

    def save_config(self):
        config_file = self.__write_config_file()
        logger.info(f'Saving config to "{config_file.name}"')
        logger.debug(f"Config: {self._config}")
        yaml.dump(
            self._config,
            config_file,
            default_flow_style=False,
            allow_unicode=True,
        )

    def get_alarm_enabled(self):
        return self._config.get("alarm_enabled", CONFIG_DEFAULTS["alarm_enabled"])

    def set_alarm_enabled(self, enabled: bool):
        self._config["alarm_enabled"] = enabled

    def toggle_alarm_enabled(self):
        self._config["alarm_enabled"] = not self.get_alarm_enabled()

    def get_alarm_time(self):
        return self._config.get("alarm_time", CONFIG_DEFAULTS["alarm_time"])

    def set_alarm_time(self, hour: int, minute: int):
        self._config["alarm_time"] = {"hour": hour, "minute": minute}
        self.update_alarm_next_datetime()

    def next_alarm_datetime(self):
        return self._next_alarm_datetime
