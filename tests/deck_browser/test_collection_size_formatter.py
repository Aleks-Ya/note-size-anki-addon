from anki.collection import Collection
from bs4 import BeautifulSoup

from note_size.deck_browser.collection_size_formatter import CollectionSizeFormatter
from tests.data import Data


def test_format_note_detailed_text(col: Collection, td: Data, collection_size_formatter: CollectionSizeFormatter):
    td.create_note_with_files()
    td.create_note_without_files()
    exp_html: str = f"""
        <div>
            <span title='Size of file "{col.path}"'>
                Collection:&nbsp;
                <span style='font-family:Consolas,monospace'>4.0 KB</span>&nbsp;&nbsp;&nbsp;
            </span>
            <span title='Size of folder "{col.media.dir()}" (3 files)'>
                Media:&nbsp;
                <span style='font-family:Consolas,monospace'>0 B</span>&nbsp;&nbsp;&nbsp;
            </span>
            <span title='Total size of collection file and media folder'>
                Total:&nbsp;
                <span style='font-family:Consolas,monospace'>4.0 KB</span>
            </span>
            <img height="12" onclick="pycmd('open-config-action')" 
            src="/_addons/1188705668/web/setting.png" title="Open Configuration"/>
        </div>
        """
    exp_soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
    exp_text: str = str(exp_soup.prettify())
    act_html: str = collection_size_formatter.format_collection_size_html()
    assert act_html == exp_text
