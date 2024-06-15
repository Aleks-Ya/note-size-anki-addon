import os
import shutil
import subprocess
from pathlib import Path

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

from setuptools import Command

version_file: str = os.path.join(os.path.dirname(__file__), 'note_size', 'version.txt')
with open(version_file, 'r') as f:
    version = f.read().strip()


class MakeDistributionCommand(Command):
    user_options = []
    project_dir: Path
    build_dir: Path

    def initialize_options(self):
        self.project_dir: Path = Path(__file__).parent
        self.build_dir: Path = Path(self.project_dir, 'dist')
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)

    def finalize_options(self):
        pass

    def run(self):
        print("Testing...")
        result = subprocess.run(['tox'], capture_output=True, text=True)
        if result.returncode != 0:
            raise SystemExit(result.returncode)

        print("Packaging...")
        note_size_dir: str = 'note_size'
        note_size_package_dir: Path = Path(self.project_dir, note_size_dir)
        dest_subdir: Path = Path(self.build_dir, note_size_dir)
        shutil.copytree(note_size_package_dir, dest_subdir,
                        ignore=shutil.ignore_patterns("*.log", "__pycache__", "meta.json"))

        self._copy_file_to_build("LICENSE", dest_subdir)
        self._copy_file_to_build("README.md", dest_subdir)

        output_zip: Path = Path(self.build_dir, f'note-size-{version}')
        actual_output_zip: Path = Path(shutil.make_archive(str(output_zip), 'zip', dest_subdir))
        renamed_output_zip: Path = Path(actual_output_zip.parent, f"{actual_output_zip.stem}.ankiaddon")
        os.rename(actual_output_zip, renamed_output_zip)
        print(f'Output ZIP: {renamed_output_zip}')

    def _copy_file_to_build(self, filename: str, dest_subdir):
        src: Path = Path(self.project_dir, filename)
        dest: Path = Path(dest_subdir, filename)
        shutil.copyfile(src, dest)


setuptools.setup(
    name="note_size_anki_addon",
    version=version,
    author="Alexey Yablokov",
    description="Note Size Anki addon",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aleks-Ya/note-size-anki-addon",
    packages=list(),
    test_suite="tests",
    cmdclass={
        'dist': MakeDistributionCommand,
    },
)
