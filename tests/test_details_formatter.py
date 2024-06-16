import tempfile
import unittest
from pathlib import Path

from anki.collection import Collection
from anki.notes import Note
from bs4 import BeautifulSoup

from note_size.details_formatter import DetailsFormatter
from tests.data import TestData


class DetailsFormatterTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.td: TestData = TestData()
        self.note_size_dir: Path = Path("../note_size").absolute() if Path("../note_size").exists() else Path("./note_size").absolute()
        self.details_formatter: DetailsFormatter = DetailsFormatter(self.note_size_dir)

    def test_format_note_detailed_text(self):
        self.note: Note = self.td.create_note_with_files(self.col)
        exp_html: str = f"""
                    <h3>Total note size: <code style="font-family:Consolas,monospace">142B</code></h3>
                    <li>Texts size: <code style="font-family:Consolas,monospace">121B</code></li>
                    <li>Files size: <code style="font-family:Consolas,monospace">21B</code></li>
                    <li>Files (big to small):</li>
                    <ol>
                        <li style="white-space:nowrap">
                            <img height="15" src="{self.note_size_dir}/icon/image.png" style="vertical-align: middle;"/>
                            animation.gif: <code style="font-family:Consolas,monospace">9B</code>
                        </li>
                        <li style="white-space:nowrap">
                            <img height="15" src="{self.note_size_dir}/icon/image.png" style="vertical-align: middle;"/>
                            picture.jpg: <code style="font-family:Consolas,monospace">7B</code>
                        </li>
                        <li style="white-space:nowrap">
                            <img height="15" src="{self.note_size_dir}/icon/audio.png" style="vertical-align: middle;"/>
                            sound.mp3: <code style="font-family:Consolas,monospace">5B</code>
                        </li>
                    </ol>
                    """
        soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        act_text: str = self.details_formatter.format_note_detailed_text(self.note)
        exp_text: str = str(soup.prettify())
        self.assertEqual(exp_text, act_text)

    def test_format_no_files(self):
        self.note: Note = self.td.create_note_without_files(self.col)
        exp_html: str = """
                    <h3>Total note size: <code style="font-family:Consolas,monospace">70B</code></h3>
                    <li>Texts size: <code style="font-family:Consolas,monospace">70B</code></li>
                    <li>Files size: <code style="font-family:Consolas,monospace">0B</code></li>
                    <li>Files: (no files)</li>
                    """
        soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        act_text: str = self.details_formatter.format_note_detailed_text(self.note)
        exp_text: str = str(soup.prettify())
        self.assertEqual(exp_text, act_text)

    def test_format_note_with_single_missing_file(self):
        self.note: Note = self.td.create_note_without_files(self.col)
        self.note[self.td.front_field_name] = 'Missing file: <img src="absents.png">'
        self.col.update_note(self.note)
        exp_html: str = f"""
                        <h3>Total note size: <code style="font-family:Consolas,monospace">73B</code></h3>
                        <li>Texts size: <code style="font-family:Consolas,monospace">73B</code></li>
                        <li>Files size: <code style="font-family:Consolas,monospace">0B</code></li>
                        <li>Files (big to small):</li>
                        <ol>
                            <li style="white-space:nowrap">
                                <img height="15" src="{self.note_size_dir}/icon/image.png" style="vertical-align: middle;"/>
                                absents.png: <code style="font-family:Consolas,monospace">0B</code>
                            </li>
                        </ol>
                        """
        soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        act_text: str = self.details_formatter.format_note_detailed_text(self.note)
        exp_text: str = str(soup.prettify())
        self.assertEqual(exp_text, act_text)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
