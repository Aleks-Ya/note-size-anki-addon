import os
import timeit
from pathlib import Path

import pytest
from anki.collection import Collection
from bs4 import BeautifulSoup

from note_size.cache.item_id_cache import ItemIdCache
from note_size.calculator.size_formatter import SizeFormatter
from note_size.ui.deck_browser.deck_browser_formatter import DeckBrowserFormatter
from note_size.ui.deck_browser.trash import Trash
from note_size.common.types import MediaFile, SizeBytes
from tests.data import Data, Digits

web_path: str = os.path.join("_addons", "1188705668", "ui", "web")
info_png_path: str = os.path.join(web_path, "info_black.png")
settings_png_path: str = os.path.join(web_path, "setting_black.png")


def test_format_note_detailed_text(col: Collection, td: Data, deck_browser_formatter: DeckBrowserFormatter,
                                   item_id_cache: ItemIdCache, media_trash_dir: Path, trash: Trash):
    item_id_cache.set_initialized(True)
    td.write_file(MediaFile("unused_file.jpg"), "unused content")
    trash_file: MediaFile = MediaFile("trashed_file.jpg")
    td.write_file(trash_file, "trash content")
    col.media.trash_files([trash_file])
    td.create_note_with_files()
    td.create_note_without_files()
    exp_html: str = f"""
    <div>
        <span style='margin-right: 0.5em;' title='Size of 2 notes in file "{col.path}"'>
            Collection:&nbsp;
            <span style='font-family:Consolas,monospace;display: inline-block;'>4.0</span>&nbsp;&nbsp;&nbsp;
            <span style="font-family:Consolas,monospace;display: inline-block;">KB</span>
        </span>
        <span style='margin-right: 0.5em;' 
            title='Size of 3 media files (3 existing and 0 missing) used in 2 notes (not include Unused and Trash)\nFolder "{col.media.dir()}"'>
            Media:&nbsp;
            <span style='font-family:Consolas,monospace;display: inline-block;'>21</span>&nbsp;&nbsp;&nbsp;
            <span style="font-family:Consolas,monospace;display: inline-block;">B</span>
        </span>
        <span style='margin-right: 0.5em;' title='Size of 1 media files not used in any notes (can be moved to Trash)'>
            Unused:&nbsp;
            <span style='font-family:Consolas,monospace;display: inline-block;'>14</span>&nbsp;&nbsp;&nbsp;
            <span style="font-family:Consolas,monospace;display: inline-block;">B</span>
        <img height="12" onclick="pycmd(\'open-check-media-action\')"
         src="{info_png_path}" style="margin-right: 0.2em;" 
         title="Click to show details"/>
         </span>
        <span style='margin-right: 0.5em;' 
            title='Size of 1 media files in the Trash (can be emptied)\nFolder "{media_trash_dir}"'>
            Trash:&nbsp;
            <span style='font-family:Consolas,monospace;display: inline-block;'>13</span>&nbsp;&nbsp;&nbsp;
            <span style="font-family:Consolas,monospace;display: inline-block;">B</span>
        <img height="12" onclick="pycmd(\'open-check-media-action\')"
         src="{info_png_path}" style="margin-right: 0.2em;" 
         title="Click to show details"/>
         </span>
        <span style='margin-right: 0.5em;' title='Total size of collection, media files, unused files and trash files'>
            Total:&nbsp;
            <span style='font-family:Consolas,monospace;display: inline-block;'>4.0</span>
            <span style="font-family:Consolas,monospace;display: inline-block;">KB</span>
        </span>
        <img height="12" onclick="pycmd('open-config-action')" 
        src="{settings_png_path}" title="Open Configuration"/>
    </div>
    """
    exp_soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
    act_soup: BeautifulSoup = BeautifulSoup(deck_browser_formatter.format_collection_size_html(), 'html.parser')
    assert act_soup.prettify() == exp_soup.prettify()


def test_item_id_cache_not_initialized(col: Collection, td: Data, deck_browser_formatter: DeckBrowserFormatter,
                                       item_id_cache: ItemIdCache, media_trash_dir: Path):
    item_id_cache.set_initialized(False)
    td.write_file(MediaFile("unused_file.jpg"), "abc")
    td.create_note_with_files()
    td.create_note_without_files()
    exp_html: str = f"""
    <div>
        <span style='margin-right: 0.5em;' title='Size of ⏳ notes in file "{col.path}"'>
            Collection:&nbsp;
            <span style='font-size: 80%'>⏳</span>&nbsp;&nbsp;&nbsp;
        </span>
        <span style='margin-right: 0.5em;' 
            title='Size of ⏳ media files (⏳ existing and ⏳ missing) used in ⏳ notes (not include Unused and Trash)\nFolder "{col.media.dir()}"'>
            Media:&nbsp;
            <span style='font-size: 80%'>⏳</span>&nbsp;&nbsp;&nbsp;
        </span>
        <span style='margin-right: 0.5em;' title='Size of ⏳ media files not used in any notes (can be moved to Trash)'>
            Unused:&nbsp;
            <span style='font-size: 80%'>⏳</span>&nbsp;&nbsp;&nbsp;
         </span>
        <span style='margin-right: 0.5em;' 
            title='Size of ⏳ media files in the Trash (can be emptied)\nFolder "{media_trash_dir}"'>
            Trash:&nbsp;
            <span style='font-size: 80%'>⏳</span>&nbsp;&nbsp;&nbsp;
         </span>
        <span style='margin-right: 0.5em;' title='Total size of collection, media files, unused files and trash files'>
            Total:&nbsp;
            <span style='font-size: 80%'>⏳</span>
        </span>
        <img height="12" onclick="pycmd('open-config-action')" 
        src="{settings_png_path}" title="Open Configuration"/>
    </div>
    """
    exp: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
    act: BeautifulSoup = BeautifulSoup(deck_browser_formatter.format_collection_size_html(), 'html.parser')
    assert exp.prettify() == act.prettify()


def test_empty_unused_and_trash(col: Collection, td: Data, deck_browser_formatter: DeckBrowserFormatter,
                                item_id_cache: ItemIdCache, media_trash_dir: Path, trash: Trash):
    item_id_cache.set_initialized(True)
    td.create_note_with_files()
    td.create_note_without_files()
    exp_html: str = f"""
    <div>
        <span style='margin-right: 0.5em;' title='Size of 2 notes in file "{col.path}"'>
            Collection:&nbsp;
            <span style='font-family:Consolas,monospace;display: inline-block;'>4.0</span>&nbsp;&nbsp;&nbsp;
            <span style="font-family:Consolas,monospace;display: inline-block;">KB</span>
        </span>
        <span style='margin-right: 0.5em;' 
            title='Size of 3 media files (3 existing and 0 missing) used in 2 notes (not include Unused and Trash)\nFolder "{col.media.dir()}"'>
            Media:&nbsp;
            <span style='font-family:Consolas,monospace;display: inline-block;'>21</span>&nbsp;&nbsp;&nbsp;
            <span style="font-family:Consolas,monospace;display: inline-block;">B</span>
        </span>
        <span style='margin-right: 0.5em;' title='Size of 0 media files not used in any notes (can be moved to Trash)'>
            Unused:&nbsp;
            <span style='font-family:Consolas,monospace;display: inline-block;'>0</span>&nbsp;&nbsp;&nbsp;
            <span style="font-family:Consolas,monospace;display: inline-block;">B</span>
        <img height="12" onclick="pycmd(\'open-check-media-action\')"
         src="{info_png_path}" style="margin-right: 0.2em;" 
         title="Click to show details"/>
         </span>
        <span style='margin-right: 0.5em;' 
            title='Size of 0 media files in the Trash (can be emptied)\nFolder "{media_trash_dir}"'>
            Trash:&nbsp;
            <span style='font-family:Consolas,monospace;display: inline-block;'>0</span>&nbsp;&nbsp;&nbsp;
            <span style="font-family:Consolas,monospace;display: inline-block;">B</span>
        <img height="12" onclick="pycmd(\'open-check-media-action\')"
         src="{info_png_path}" style="margin-right: 0.2em;" 
         title="Click to show details"/>
         </span>
        <span style='margin-right: 0.5em;' title='Total size of collection, media files, unused files and trash files'>
            Total:&nbsp;
            <span style='font-family:Consolas,monospace;display: inline-block;'>4.0</span>
            <span style="font-family:Consolas,monospace;display: inline-block;">KB</span>
        </span>
        <img height="12" onclick="pycmd('open-config-action')" 
        src="{settings_png_path}" title="Open Configuration"/>
    </div>
    """
    exp_soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
    act_soup: BeautifulSoup = BeautifulSoup(deck_browser_formatter.format_collection_size_html(), 'html.parser')
    assert act_soup.prettify() == exp_soup.prettify()


@pytest.mark.performance
def test_bytes_to_str_performance(size_formatter: SizeFormatter):
    size_bytes: SizeBytes = SizeBytes(123_456_789)
    execution_time: float = timeit.timeit(lambda: size_formatter.bytes_to_str(size_bytes, Digits.one),
                                          number=300_000)
    assert execution_time <= 1
