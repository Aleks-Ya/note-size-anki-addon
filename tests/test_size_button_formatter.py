import tempfile
import textwrap
import unittest

from anki.collection import Collection

from note_size.size_button_formatter import SizeButtonFormatter
from tests.data import TestData


class SizeButtonFormatterTestCase(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.td: TestData = TestData()
        self.note = self.td.create_note(self.col)

    def test_total_text_size(self):
        act_text: str = SizeButtonFormatter.format_note_detailed_text(self.note)
        exp_text: str = textwrap.dedent("""
        <h3>Total note size: 129B</h3>
        <ul>
            <li>Texts size: 108B</li>
            <li>Files size: 21B</li>
            <li>Files (big to small):</li>
                <ol>
                    <li style="white-space:nowrap">animation.gif: 9B</li><li style="white-space:nowrap">picture.jpg: 7B</li><li style="white-space:nowrap">sound.mp3: 5B</li>
                </ol>
        </ul>
        """)
        self.assertEqual(exp_text, act_text)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
