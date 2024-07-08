import tempfile
import unittest

from anki.collection import Collection
from bs4 import BeautifulSoup

from note_size.config.config import Config
from note_size.cache.media_cache import MediaCache
from note_size.deck_browser.collection_size_formatter import CollectionSizeFormatter
from tests.data import Data


class TestCollectionSizeFormatter(unittest.TestCase):

    def setUp(self):
        self.col: Collection = Collection(tempfile.mkstemp(suffix=".anki2")[1])
        self.td: Data = Data(self.col)
        config: Config = Data.read_config()
        media_cache: MediaCache = MediaCache(self.col, config)
        self.collection_size_formatter: CollectionSizeFormatter = CollectionSizeFormatter(self.col, media_cache)

    def test_format_note_detailed_text(self):
        self.td.create_note_with_files()
        self.td.create_note_without_files()
        exp_html: str = f"""
            <div>
                <span title='Size of file "{self.col.path}"'>
                    Collection:&nbsp;
                    <span style='font-family:Consolas,monospace'>4.0KB</span>&nbsp;&nbsp;&nbsp;
                </span>
                <span title='Size of folder "{self.col.media.dir()}" (3 files)'>
                    Media:&nbsp;
                    <span style='font-family:Consolas,monospace'>0B</span>&nbsp;&nbsp;&nbsp;
                </span>
                <span title='Total size of collection file and media folder'>
                    Total:&nbsp;
                    <span style='font-family:Consolas,monospace'>4.0KB</span>
                </span>
            </div>
            """
        exp_soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
        exp_text: str = str(exp_soup.prettify())
        act_html: str = self.collection_size_formatter.format_collection_size_html()
        self.assertEqual(exp_text, act_html)

    def tearDown(self):
        self.col.close()


if __name__ == '__main__':
    unittest.main()
