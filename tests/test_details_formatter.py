import tempfile
import unittest

from anki.collection import Collection
from anki.notes import Note
from bs4 import BeautifulSoup

from note_size.details_formatter import DetailsFormatter
from tests.data import TestData


class DetailsFormatterTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.td: TestData = TestData()

    def test_format_note_detailed_text(self):
        self.note: Note = self.td.create_note_with_files(self.col)
        exp_html: str = """
                    <h3>Total note size: <code>142B</code></h3>
                    <li>Texts size: <code>121B</code></li>
                    <li>Files size: <code>21B</code></li>
                    <li>Files (big to small):</li>
                    <ol>
                        <li style="white-space:nowrap">animation.gif: <code>9B</code></li>
                        <li style="white-space:nowrap">picture.jpg: <code>7B</code></li>
                        <li style="white-space:nowrap">sound.mp3: <code>5B</code></li>
                    </ol>
                    """
        soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        act_text: str = DetailsFormatter.format_note_detailed_text(self.note)
        exp_text: str = str(soup.prettify())
        self.assertEqual(exp_text, act_text)

    def test_format_no_files(self):
        self.note: Note = self.td.create_note_without_files(self.col)
        exp_html: str = """
                    <h3>Total note size: <code>70B</code></h3>
                    <li>Texts size: <code>70B</code></li>
                    <li>Files size: <code>0B</code></li>
                    <li>Files: (no files)</li>
                    """
        soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        act_text: str = DetailsFormatter.format_note_detailed_text(self.note)
        exp_text: str = str(soup.prettify())
        self.assertEqual(exp_text, act_text)

    def test_format_note_with_single_missing_file(self):
        self.note: Note = self.td.create_note_without_files(self.col)
        self.note[self.td.front_field_name] = 'Missing file: <img src="absents.png">'
        self.col.update_note(self.note)
        exp_html: str = """
                        <h3>Total note size: <code>73B</code></h3>
                        <li>Texts size: <code>73B</code></li>
                        <li>Files size: <code>0B</code></li>
                        <li>Files (big to small):</li>
                        <ol>
                            <li style="white-space:nowrap">absents.png: <code>0B</code></li>
                        </ol>
                        """
        soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        act_text: str = DetailsFormatter.format_note_detailed_text(self.note)
        exp_text: str = str(soup.prettify())
        self.assertEqual(exp_text, act_text)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
