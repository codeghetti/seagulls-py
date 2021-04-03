import logging
import logging.config
from typing import Dict, Any

logger = logging.getLogger(__name__)


class LoggingClient:

    _verbosity: int

    def __init__(self, verbosity: int):
        self._verbosity = verbosity

    def configure_logging(self) -> None:
        logging.config.dictConfig(self._get_config())

    def _get_config(self) -> Dict[Any, Any]:
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "colored": {
                    "()": "colorlog.ColoredFormatter",
                    "format": (
                        "%(log_color)s%(asctime)s %(levelname)-8s [%(name)s][%(lineno)d]: "
                        "%(reset)s%(blue)s%(message)s"
                    ),
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "log_colors": {
                        "DEBUG": "cyan",
                        "INFO": "green",
                        "WARNING": "yellow",
                        "ERROR": "red",
                        "CRITICAL": "bold_red",
                    },
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "stream": "ext://sys.stderr",
                    "formatter": "colored",
                }
            },
            "loggers": {
                "seagulls": {
                    "level": self._get_app_log_level(),
                    "handlers": ["console"],
                    "propagate": False,
                }
            },
            "root": {
                "level": self._get_root_log_level(),
                "handlers": ["console"],
            }
        }

    def _get_root_log_level(self) -> str:
        return {
            0: "CRITICAL",
            1: "ERROR",
            2: "ERROR",
            3: "WARNING",
            4: "WARNING",
            5: "INFO",
            6: "DEBUG",
        }[min(self.get_verbosity(), 6)]

    def _get_app_log_level(self) -> str:
        return {
            0: "CRITICAL",
            1: "ERROR",
            2: "WARNING",
            3: "INFO",
            4: "DEBUG",
            5: "DEBUG",
            6: "DEBUG",
        }[min(self.get_verbosity(), 6)]

    def get_verbosity(self) -> int:
        return self._verbosity
