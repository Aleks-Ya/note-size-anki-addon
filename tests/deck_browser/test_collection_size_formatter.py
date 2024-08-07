from anki.collection import Collection
from bs4 import BeautifulSoup

from note_size.cache.item_id_cache import ItemIdCache
from note_size.deck_browser.collection_size_formatter import CollectionSizeFormatter
from note_size.types import MediaFile
from tests.data import Data


def test_format_note_detailed_text(col: Collection, td: Data, collection_size_formatter: CollectionSizeFormatter,
                                   item_id_cache: ItemIdCache):
    item_id_cache.set_initialized(True)
    td.write_file(MediaFile("unused_file.jpg"), "abc")
    td.create_note_with_files()
    td.create_note_without_files()
    exp_html: str = f"""
    <div>
        <span style='margin-right: 0.5em;' title='Size of 2 notes\nFile "{col.path}"'>
            Collection:&nbsp;
            <span style='font-family:Consolas,monospace;display: inline-block;'>4</span>&nbsp;&nbsp;&nbsp;
            <span style="font-family:Consolas,monospace;display: inline-block;">KB</span>
        </span>
        <span style='margin-right: 0.5em;' 
            title='Size of 3 media files used in notes (not include Unused and Trash)\nFolder "{col.media.dir()}"'>
            Media:&nbsp;
            <span style='font-family:Consolas,monospace;display: inline-block;'>21</span>&nbsp;&nbsp;&nbsp;
            <span style="font-family:Consolas,monospace;display: inline-block;">B</span>
        </span>
        <span style='margin-right: 0.5em;' title='Size of 1 media files not used in any notes (can be moved to Trash)'>
            Unused:&nbsp;
            <span style='font-family:Consolas,monospace;display: inline-block;'>3</span>&nbsp;&nbsp;&nbsp;
            <span style="font-family:Consolas,monospace;display: inline-block;">B</span>
        <img height="12" onclick="pycmd(\'open-check-media-action\')"
         src="/_addons/1188705668/web/info.png" style="margin-left: -0.2em; margin-right: 0.2em;" 
         title="Click to show details"/>
         </span>
        <span style='margin-right: 0.5em;' 
            title='Size of 1 media files in the Trash (can be emptied)\nFolder "/tmp/media.trash"'>
            Trash:&nbsp;
            <span style='font-family:Consolas,monospace;display: inline-block;'>6</span>&nbsp;&nbsp;&nbsp;
            <span style="font-family:Consolas,monospace;display: inline-block;">B</span>
        <img height="12" onclick="pycmd(\'open-check-media-action\')"
         src="/_addons/1188705668/web/info.png" style="margin-left: -0.2em; margin-right: 0.2em;" 
         title="Click to show details"/>
         </span>
        <span style='margin-right: 0.5em;' title='Total size of collection, media files, unused files and trash files'>
            Total:&nbsp;
            <span style='font-family:Consolas,monospace;display: inline-block;'>4</span>
            <span style="font-family:Consolas,monospace;display: inline-block;">KB</span>
        </span>
        <img height="12" onclick="pycmd('open-config-action')" 
        src="/_addons/1188705668/web/setting.png" title="Open Configuration"/>
    </div>
    """
    exp_soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
    exp_text: str = str(exp_soup.prettify())
    act_html: str = collection_size_formatter.format_collection_size_html()
    assert act_html == exp_text


def test_item_id_cache_not_initialized(col: Collection, td: Data, collection_size_formatter: CollectionSizeFormatter,
                                       item_id_cache: ItemIdCache):
    item_id_cache.set_initialized(False)
    td.write_file(MediaFile("unused_file.jpg"), "abc")
    td.create_note_with_files()
    td.create_note_without_files()
    exp_html: str = f"""
    <div>
        <span style='margin-right: 0.5em;' title='Size of ⏳ notes\nFile "{col.path}"'>
            Collection:&nbsp;
            <span style='font-size: 80%'>⏳</span>&nbsp;&nbsp;&nbsp;
        </span>
        <span style='margin-right: 0.5em;' 
            title='Size of ⏳ media files used in notes (not include Unused and Trash)\nFolder "{col.media.dir()}"'>
            Media:&nbsp;
            <span style='font-size: 80%'>⏳</span>&nbsp;&nbsp;&nbsp;
        </span>
        <span style='margin-right: 0.5em;' title='Size of ⏳ media files not used in any notes (can be moved to Trash)'>
            Unused:&nbsp;
            <span style='font-size: 80%'>⏳</span>&nbsp;&nbsp;&nbsp;
         </span>
        <span style='margin-right: 0.5em;' 
            title='Size of ⏳ media files in the Trash (can be emptied)\nFolder "/tmp/media.trash"'>
            Trash:&nbsp;
            <span style='font-size: 80%'>⏳</span>&nbsp;&nbsp;&nbsp;
         </span>
        <span style='margin-right: 0.5em;' title='Total size of collection, media files, unused files and trash files'>
            Total:&nbsp;
            <span style='font-size: 80%'>⏳</span>
        </span>
        <img height="12" onclick="pycmd('open-config-action')" 
        src="/_addons/1188705668/web/setting.png" title="Open Configuration"/>
    </div>
    """
    exp_soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
    exp_text: str = str(exp_soup.prettify())
    act_html: str = collection_size_formatter.format_collection_size_html()
    assert act_html == exp_text
