import shutil
import subprocess
from pathlib import Path

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

from setuptools import Command

version = "1.0.1"


class MakeDistributionCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("Testing...")
        result = subprocess.run(['tox'], capture_output=True, text=True)
        if result.returncode != 0:
            raise SystemExit(result.returncode)

        print("Packaging...")
        project_dir: Path = Path(__file__).parent
        build_dir: Path = Path(project_dir, 'dist')
        if build_dir.exists():
            shutil.rmtree(build_dir)
        note_size_dir: str = 'note_size'
        note_size_package_dir: Path = Path(project_dir, note_size_dir)
        dest_subdir: Path = Path(build_dir, note_size_dir)
        shutil.copytree(note_size_package_dir, dest_subdir, ignore=shutil.ignore_patterns("*.log"))

        license_filename: str = "LICENSE"
        license_file_src: Path = Path(project_dir, license_filename)
        license_file_dest: Path = Path(dest_subdir, license_filename)
        shutil.copyfile(license_file_src, license_file_dest)

        readme_filename: str = "README.md"
        readme_file_src: Path = Path(project_dir, readme_filename)
        readme_file_dest: Path = Path(dest_subdir, readme_filename)
        shutil.copyfile(readme_file_src, readme_file_dest)

        output_zip: Path = Path(build_dir, f'note-size-{version}')
        actual_output_zip: str = shutil.make_archive(str(output_zip), 'zip', dest_subdir)
        print(f'Output ZIP: {actual_output_zip}')


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
