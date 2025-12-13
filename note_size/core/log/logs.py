import logging
from logging import Logger, FileHandler, Formatter
from pathlib import Path

from ..config.settings import Settings


class Logs:
    def __init__(self, settings: Settings):
        log_dir: Path = settings.logs_folder
        log_dir.mkdir(exist_ok=True, parents=True)
        self.__log_file: Path = log_dir.joinpath("note_size.log")
        self.__root_logger: Logger = self.__configure_logging()

    def root_logger(self) -> Logger:
        return self.__root_logger

    def set_level(self, log_level: str) -> None:
        self.__root_logger.setLevel(log_level)

    def get_log_file(self) -> Path:
        return self.__log_file

    def __configure_logging(self) -> Logger:
        logger: Logger = logging.getLogger(__name__.split(".")[0])
        handler: FileHandler = FileHandler(self.__log_file, encoding="utf-8", errors="replace")
        level: int = logging.DEBUG
        handler.setLevel(level)
        formatter: Formatter = Formatter('%(asctime)s %(levelname)s %(name)s %(funcName)s %(threadName)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
        logger.info(f"\n\n{'#' * 100}\nLogger was configured: "
                    f"logger_name={logger.name}, level={logging.getLevelName(level)}, file={self.__log_file}")
        return logger
