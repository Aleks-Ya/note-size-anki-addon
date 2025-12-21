from pathlib import Path

from note_size.core.config.settings import Settings


def test_to_string(settings: Settings, module_dir: Path):
    assert str(settings) == f"""Settings(module_dir={module_dir}, module_name=1188705668)"""


def test_addon_version(settings: Settings):
    assert settings.addon_version == "2.11.0"
