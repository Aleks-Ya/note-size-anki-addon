import tempfile
import unittest

from anki.collection import Collection
from anki.notes import Note
from bs4 import BeautifulSoup

from note_size import SizeCalculator
from note_size.size_button_formatter import SizeButtonFormatter
from tests.data import TestData


class SizeButtonFormatterTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.td: TestData = TestData()
        size_calculator: SizeCalculator = SizeCalculator()
        self.size_button_formatter: SizeButtonFormatter = SizeButtonFormatter(size_calculator)

    def test_format_note_detailed_text(self):
        self.note: Note = self.td.create_note_with_files(self.col)
        exp_html: str = """
                    <h3>Total note size: 129B</h3>
                    <li>Texts size: 108B</li>
                    <li>Files size: 21B</li>
                    <li>Files (big to small):</li>
                    <ol>
                        <li style="white-space:nowrap">animation.gif: 9B</li>
                        <li style="white-space:nowrap">picture.jpg: 7B</li>
                        <li style="white-space:nowrap">sound.mp3: 5B</li>
                    </ol>
                    """
        soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        act_text: str = self.size_button_formatter.format_note_detailed_text(self.note)
        exp_text: str = str(soup.prettify())
        self.assertEqual(exp_text, act_text)

    def test_format_no_files(self):
        self.note: Note = self.td.create_note_without_files(self.col)
        exp_html: str = """
                    <h3>Total note size: 57B</h3>
                    <li>Texts size: 57B</li>
                    <li>Files size: 0B</li>
                    <li>Files: (no files)</li>
                    """
        soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        act_text: str = self.size_button_formatter.format_note_detailed_text(self.note)
        exp_text: str = str(soup.prettify())
        self.assertEqual(exp_text, act_text)

    def test_format_note_with_single_missing_file(self):
        self.note: Note = self.td.create_note_without_files(self.col)
        self.note[self.td.front_field_name] = 'Missing file: <img src="absents.png">'
        exp_html: str = """
                        <h3>Total note size: 67B</h3>
                        <li>Texts size: 67B</li>
                        <li>Files size: 0B</li>
                        <li>Files (big to small):</li>
                        <ol>
                            <li style="white-space:nowrap">absents.png: 0B</li>
                        </ol>
                        """
        soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        act_text: str = self.size_button_formatter.format_note_detailed_text(self.note)
        exp_text: str = str(soup.prettify())
        self.assertEqual(exp_text, act_text)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
