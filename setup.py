import os
import shutil
import subprocess

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

from setuptools import Command

version = "1.0"


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
        project_dir: str = os.path.abspath(os.path.dirname(__file__))
        build_dir: str = os.path.join(project_dir, 'dist')
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
        note_size_dir: str = 'note_size'
        note_size_package_dir: str = os.path.join(project_dir, note_size_dir)
        dest_subdir: str = os.path.join(build_dir, note_size_dir)
        shutil.copytree(note_size_package_dir, dest_subdir, ignore=shutil.ignore_patterns("*.log"))

        license_filename: str = "LICENSE"
        license_file_src: str = os.path.join(project_dir, license_filename)
        license_file_dest: str = os.path.join(dest_subdir, license_filename)
        shutil.copyfile(license_file_src, license_file_dest)

        readme_filename: str = "README.md"
        readme_file_src: str = os.path.join(project_dir, readme_filename)
        readme_file_dest: str = os.path.join(dest_subdir, readme_filename)
        shutil.copyfile(readme_file_src, readme_file_dest)

        output_zip: str = os.path.join(build_dir, f'note-size-{version}')
        shutil.make_archive(output_zip, 'zip', dest_subdir)
        print(f'Output ZIP: {output_zip}')


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
        'distribution_command': MakeDistributionCommand,
    },
)
