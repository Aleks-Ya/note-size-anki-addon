import json
import os
import shutil
import subprocess
from pathlib import Path
from subprocess import CompletedProcess

_version = "2.6.1"
_author = "Alexey Yablokov"


class DistributionBuilder:

    def __init__(self):
        self.project_dir: Path = Path(__file__).parent
        self.build_dir: Path = Path(self.project_dir, 'dist')
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)

    def build(self) -> None:
        self.__run_unit_tests()
        self.__run_integration_tests()
        self.__package_zip()

    @staticmethod
    def __run_unit_tests() -> None:
        print("Running unit tests...")
        result: CompletedProcess[str] = subprocess.run(['tox'], capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stderr)
            print(result.stdout)
            raise SystemExit(result.returncode)

    @staticmethod
    def __run_integration_tests() -> None:
        print("Running integration tests...")
        result: CompletedProcess[str] = subprocess.run(
            ['tox', '-e', 'integration'], capture_output=True, text=True)
        if result.returncode == 5:
            print("No integration tests found")
        elif result.returncode != 0:
            print(result.stderr)
            print(result.stdout)
            raise SystemExit(result.returncode)

    def __package_zip(self) -> None:
        print("Packaging...")
        addon_dir: str = 'note_size'
        addon_package_dir: Path = Path(self.project_dir, addon_dir)
        dest_subdir: Path = Path(self.build_dir, addon_dir)
        shutil.copytree(addon_package_dir, dest_subdir,
                        ignore=shutil.ignore_patterns("*.log", "__pycache__", "meta.json"))
        self.__generate_manifest(dest_subdir)
        self.__copy_file_to_build("LICENSE", dest_subdir)
        self.__copy_file_to_build("README.md", dest_subdir)
        self.__copy_file_to_build("CHANGELOG.md", dest_subdir)
        output_zip: Path = Path(self.build_dir, f'note-size-{_version}')
        actual_output_zip: Path = Path(shutil.make_archive(str(output_zip), 'zip', dest_subdir))
        renamed_output_zip: Path = Path(actual_output_zip.parent, f"{actual_output_zip.stem}.ankiaddon")
        os.rename(actual_output_zip, renamed_output_zip)
        print(f'Output ZIP: {renamed_output_zip}')

    def __copy_file_to_build(self, filename: str, dest_subdir) -> None:
        src: Path = Path(self.project_dir, filename)
        dest: Path = Path(dest_subdir, filename)
        shutil.copyfile(src, dest)

    @staticmethod
    def __generate_manifest(dest_subdir: Path) -> None:
        from git import TagReference, Repo, Commit
        repo: Repo = Repo(".", search_parent_directories=True)
        version: str = f"v{_version}"
        tag: TagReference = repo.tag(version)
        commit: Commit = tag.commit if tag in repo.tags else repo.head.commit
        commit_epoch_sec: int = int(commit.committed_datetime.timestamp())
        draft: dict[str, any] = {
            "name": f"Note Size - sort notes by size {version}",
            "package": "1188705668",
            "author": _author,
            "min_point_version": 240401,
            "max_point_version": 240603,
            "human_version": version,
            "homepage": "https://ankiweb.net/shared/info/1188705668",
            "mod": commit_epoch_sec
        }
        path: Path = Path(dest_subdir, 'manifest.json')
        with open(path, 'w') as fp:
            # noinspection PyTypeChecker
            json.dump(draft, fp, indent=2)


dist_builder: DistributionBuilder = DistributionBuilder()
dist_builder.build()
