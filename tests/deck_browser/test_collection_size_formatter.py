from anki.collection import Collection
from bs4 import BeautifulSoup

from note_size.deck_browser.collection_size_formatter import CollectionSizeFormatter
from tests.data import Data


def test_format_note_detailed_text(col: Collection, td: Data, collection_size_formatter: CollectionSizeFormatter):
    td.create_note_with_files()
    td.create_note_without_files()
    exp_html: str = f"""
        <div>
            <span style='margin-right: 0.5em;' title='Size of file "{col.path}"'>
                Collection:&nbsp;
                <span style='font-family:Consolas,monospace;display: inline-block;'>4 KB</span>&nbsp;&nbsp;&nbsp;
            </span>
            <span style='margin-right: 0.5em;' title='Size of 3 media files used in notes (do not include "Unused" and "Trash")'>
                Media:&nbsp;
                <span style='font-family:Consolas,monospace;display: inline-block;'>21 B</span>&nbsp;&nbsp;&nbsp;
            </span>
            <span style='margin-right: 0.5em;' title='Size of 0 media files not used in any notes (can be moved to Trash)'>
                Unused:&nbsp;
                <span style='font-family:Consolas,monospace;display: inline-block;'>0 B</span>&nbsp;&nbsp;&nbsp;
            <img height="12" onclick="pycmd(\'open-check-media-action\')"
             src="/_addons/1188705668/web/info.png" style="margin-left: -0.2em; margin-right: 0.2em;" 
             title="Click to show details (open the Check Media dialog)"/>
             </span>
            <span style='margin-right: 0.5em;' title='Size of 1 media files in the Trash (can be emptied)'>
                Trash:&nbsp;
                <span style='font-family:Consolas,monospace;display: inline-block;'>6 B</span>&nbsp;&nbsp;&nbsp;
            <img height="12" onclick="pycmd(\'open-check-media-action\')"
             src="/_addons/1188705668/web/info.png" style="margin-left: -0.2em; margin-right: 0.2em;" 
             title="Click to show details (open the Check Media dialog)"/>
             </span>
            <span style='margin-right: 0.5em;' title='Total size of collection file and media folder'>
                Total:&nbsp;
                <span style='font-family:Consolas,monospace;display: inline-block;'>4 KB</span>
            </span>
            <img height="12" onclick="pycmd('open-config-action')" 
            src="/_addons/1188705668/web/setting.png" title="Open Configuration"/>
        </div>
        """
    exp_soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
    exp_text: str = str(exp_soup.prettify())
    act_html: str = collection_size_formatter.format_collection_size_html()
    assert act_html == exp_text
