import os
from pathlib import Path

from note_size.config.config import Config
from note_size.config.settings import Settings
from note_size.profiler.profiler import Profiler


def test_start_profiling_disabled(profiler: Profiler, settings: Settings, config: Config):
    assert not config.get_profiler_enabled()

    report_by_cumulative_time: Path = profiler.get_report_by_cumulative_time()
    report_by_call_number: Path = profiler.get_report_by_call_number()
    report_by_internal_time: Path = profiler.get_report_by_internal_time()

    assert not report_by_cumulative_time.exists()
    assert not report_by_call_number.exists()
    assert not report_by_internal_time.exists()

    profiler.start_profiling()
    profiler.stop_profiling()

    assert not report_by_cumulative_time.exists()
    assert not report_by_call_number.exists()
    assert not report_by_internal_time.exists()


def test_start_profiling_enabled(profiler: Profiler, settings: Settings, config: Config):
    config.set_profiler_enabled(True)

    report_by_cumulative_time: Path = profiler.get_report_by_cumulative_time()
    report_by_call_number: Path = profiler.get_report_by_call_number()
    report_by_internal_time: Path = profiler.get_report_by_internal_time()

    assert not report_by_cumulative_time.exists()
    assert not report_by_call_number.exists()
    assert not report_by_internal_time.exists()

    profiler.start_profiling()
    profiler.stop_profiling()

    assert report_by_cumulative_time.exists()
    assert report_by_call_number.exists()
    assert report_by_internal_time.exists()

    assert os.path.getsize(report_by_cumulative_time) > 0
    assert os.path.getsize(report_by_call_number) > 0
    assert os.path.getsize(report_by_internal_time) > 0
