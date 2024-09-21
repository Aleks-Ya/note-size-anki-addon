import logging
from cProfile import Profile
from logging import Logger
from pathlib import Path
from pstats import Stats, SortKey

from ..config.config import Config
from ..config.settings import Settings

log: Logger = logging.getLogger(__name__)


class Profiler:

    def __init__(self, config: Config, settings: Settings) -> None:
        self.__config: Config = config
        self.__profile: Profile = Profile()
        self.__cache_file: Path = settings.cache_file
        self.__file_by_cumulative_time: Path = settings.logs_folder.joinpath("profiler_report_by_cumulative_time.txt")
        self.__file_by_call_number: Path = settings.logs_folder.joinpath("profiler_report_by_call_number.txt")
        self.__file_by_internal_time: Path = settings.logs_folder.joinpath("profiler_report_by_internal_time.txt")
        log.debug(f"{self.__class__.__name__} was instantiated")

    def start_profiling(self) -> None:
        if self.__config.get_profiler_enabled():
            log.debug("Start profiler")
            self.__profile.enable()
        else:
            log.debug("Profiler is disabled")

    def stop_profiling(self) -> None:
        if self.__config.get_profiler_enabled():
            log.debug("Stop profiler")
            self.__profile.disable()
            log.info(f"Profile reports:\n"
                     f"{self.__file_by_cumulative_time}\n"
                     f"{self.__file_by_call_number}\n"
                     f"{self.__file_by_internal_time}")
            self.__write_report(self.__profile, self.__file_by_cumulative_time, SortKey.CUMULATIVE)
            self.__write_report(self.__profile, self.__file_by_call_number, SortKey.CALLS)
            self.__write_report(self.__profile, self.__file_by_internal_time, SortKey.TIME)
        else:
            log.debug("Profiler is disabled")

    @staticmethod
    def __write_report(profile: Profile, file: Path, sort_key: SortKey) -> None:
        with open(file, 'w') as f:
            Stats(profile, stream=f).sort_stats(sort_key).print_stats()
