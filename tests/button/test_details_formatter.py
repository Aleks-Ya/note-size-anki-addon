import tempfile
import unittest
from pathlib import Path

from anki.collection import Collection
from anki.notes import Note
from bs4 import BeautifulSoup

from note_size import Config
from note_size.calculator.size_calculator import SizeCalculator
from note_size.button.details_formatter import DetailsFormatter
from note_size.cache.media_cache import MediaCache
from note_size.types import FileContent, MediaFile, FieldName
from tests.data import Data, DefaultFields


class TestDetailsFormatter(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.td: Data = Data(self.col)
        self.addon_dir: Path = Path(__file__).parent.parent.parent.joinpath("note_size")
        config: Config = Data.read_config()
        media_cache: MediaCache = MediaCache(self.col, config)
        size_calculator: SizeCalculator = SizeCalculator(media_cache)
        self.details_formatter: DetailsFormatter = DetailsFormatter(self.addon_dir, size_calculator, config)

    def test_format_note_detailed_text(self):
        note: Note = self.td.create_note_with_files()
        exp_html: str = f"""
            <h3>Total note size: <code style="font-family:Consolas,monospace">143B</code></h3>
            <li>Texts size: <code style="font-family:Consolas,monospace">122B</code></li>
            <li>Files size: <code style="font-family:Consolas,monospace">21B</code></li>
            <li>Files (big to small):</li>
            <ol>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    animation.gif: <code style="font-family:Consolas,monospace">9B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    picture.jpg: <code style="font-family:Consolas,monospace">7B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Audio file" height="15" src="{self.addon_dir}/button/icon/audio.png" style="vertical-align: middle;"/>
                    sound.mp3: <code style="font-family:Consolas,monospace">5B</code>
                </li>
            </ol>
            """
        soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        act_text: str = self.details_formatter.format_note_detailed_text(note)
        exp_text: str = str(soup.prettify())
        self.assertEqual(exp_text, act_text)

    def test_format_no_files(self):
        note: Note = self.td.create_note_without_files()
        exp_html: str = """
                    <h3>Total note size: <code style="font-family:Consolas,monospace">70B</code></h3>
                    <li>Texts size: <code style="font-family:Consolas,monospace">70B</code></li>
                    <li>Files size: <code style="font-family:Consolas,monospace">0B</code></li>
                    <li>Files: (no files)</li>
                    """
        soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        act_text: str = self.details_formatter.format_note_detailed_text(note)
        exp_text: str = str(soup.prettify())
        self.assertEqual(exp_text, act_text)

    def test_format_note_with_single_missing_file(self):
        note: Note = self.td.create_note_without_files()
        self.td.update_front_field(note, 'Missing file: <img src="absents.png">')
        exp_html: str = f"""
            <h3>Total note size: <code style="font-family:Consolas,monospace">73B</code></h3>
            <li>Texts size: <code style="font-family:Consolas,monospace">73B</code></li>
            <li>Files size: <code style="font-family:Consolas,monospace">0B</code></li>
            <li>Files (big to small):</li>
            <ol>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    absents.png: <code style="font-family:Consolas,monospace">0B</code>
                </li>
            </ol>
                        """
        soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        act_text: str = self.details_formatter.format_note_detailed_text(note)
        exp_text: str = str(soup.prettify())
        self.assertEqual(exp_text, act_text)

    def test_unrecognized_mime_type(self):
        files: dict[FieldName, dict[MediaFile, FileContent]] = {
            DefaultFields.front_field_name: {
                MediaFile("without_extension"): DefaultFields.content0,
                MediaFile("unrecognized_extension.ae1"): DefaultFields.content1
            }
        }
        note: Note = self.td.create_note_with_given_files(files)
        exp_html: str = f"""
            <h3> Total note size: <code style="font-family:Consolas,monospace"> 94B </code></h3>
            <li> Texts size: <code style="font-family:Consolas,monospace"> 82B </code></li>
            <li> Files size: <code style="font-family:Consolas,monospace"> 12B </code></li>
            <li> Files (big to small):</li>
            <ol>
                <li style="white-space:nowrap">
                    <img alt="Other file"  height="15" src="{self.addon_dir}/button/icon/other.png" style="vertical-align: middle;"/>
                    without_extension: <code style="font-family:Consolas,monospace"> 7B </code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Other file" height="15" src="{self.addon_dir}/button/icon/other.png" style="vertical-align: middle;"/>
                    unrecognized_extension.ae1: <code style="font-family:Consolas,monospace"> 5B </code>
                </li>
            </ol>
                    """
        soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        act_text: str = self.details_formatter.format_note_detailed_text(note)
        exp_text: str = str(soup.prettify())
        self.assertEqual(exp_text, act_text)

    def test_limit_showed_number_of_files(self):
        files: dict[MediaFile, FileContent] = TestDetailsFormatter.__generate_files(15)
        fields: dict[FieldName, dict[MediaFile, FileContent]] = {
            DefaultFields.front_field_name: files
        }
        note: Note = self.td.create_note_with_given_files(fields)
        exp_html: str = f"""
            <h3>Total note size:<code style="font-family:Consolas,monospace">523B</code></h3>
            <li>Texts size:<code style="font-family:Consolas,monospace">373B</code></li>
            <li>Files size:<code style="font-family:Consolas,monospace">150B</code></li>
            <li>Files (big to small):</li>
            <ol>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_00.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_01.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_02.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_03.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_04.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_05.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_06.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_07.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_08.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_09.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">More 5 files are hidden</li>
            </ol>
                    """
        soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        act_text: str = self.details_formatter.format_note_detailed_text(note)
        exp_text: str = str(soup.prettify())
        self.assertEqual(exp_text, act_text)

    def test_limit_showed_number_of_files_exact(self):
        files: dict[MediaFile, FileContent] = TestDetailsFormatter.__generate_files(10)
        fields: dict[FieldName, dict[MediaFile, FileContent]] = {
            DefaultFields.front_field_name: files
        }
        note: Note = self.td.create_note_with_given_files(fields)
        exp_html: str = f"""
            <h3>Total note size:<code style="font-family:Consolas,monospace">353B</code></h3>
            <li>Texts size:<code style="font-family:Consolas,monospace">253B</code></li>
            <li>Files size:<code style="font-family:Consolas,monospace">100B</code></li>
            <li>Files (big to small):</li>
            <ol>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_00.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_01.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_02.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_03.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_04.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_05.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_06.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_07.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_08.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
                <li style="white-space:nowrap">
                    <img alt="Image file" height="15" src="{self.addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                    file_09.png:<code style="font-family:Consolas,monospace">10B</code>
                </li>
            </ol>
                    """
        soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        act_text: str = self.details_formatter.format_note_detailed_text(note)
        exp_text: str = str(soup.prettify())
        self.assertEqual(exp_text, act_text)

    @staticmethod
    def __generate_files(file_number):
        return {MediaFile(f"file_{i:02d}.png"): FileContent(f"content_{i:02d}") for i in range(file_number)}

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
