from pathlib import Path

from anki.notes import Note
from bs4 import BeautifulSoup

from note_size.button.details_formatter import DetailsFormatter
from note_size.types import FileContent, MediaFile, FieldName
from tests.data import Data, DefaultFields


def test_format_note_detailed_text(td: Data, addon_dir: Path, details_formatter: DetailsFormatter):
    note: Note = td.create_note_with_files()
    exp_html: str = f"""
        <h3>Total note size: <code style="font-family:Consolas,monospace">143 B</code></h3>
        <li>Texts size: <code style="font-family:Consolas,monospace">122 B</code></li>
        <li>Files size: <code style="font-family:Consolas,monospace">21 B</code></li>
        <li>Files (big to small):</li>
        <ol>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                animation.gif: <code style="font-family:Consolas,monospace">9 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                picture.jpg: <code style="font-family:Consolas,monospace">7 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Audio file" height="15" src="{addon_dir}/button/icon/audio.png" style="vertical-align: middle;"/>
                sound.mp3: <code style="font-family:Consolas,monospace">5 B</code>
            </li>
        </ol>
        """
    soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
    act_text: str = details_formatter.format_note_detailed_text(note)
    exp_text: str = str(soup.prettify())
    assert exp_text == act_text


def test_format_no_files(td: Data, details_formatter: DetailsFormatter):
    note: Note = td.create_note_without_files()
    exp_html: str = """
                <h3>Total note size: <code style="font-family:Consolas,monospace">70 B</code></h3>
                <li>Texts size: <code style="font-family:Consolas,monospace">70 B</code></li>
                <li>Files size: <code style="font-family:Consolas,monospace">0 B</code></li>
                <li>Files: (no files)</li>
                """
    soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
    act_text: str = details_formatter.format_note_detailed_text(note)
    exp_text: str = str(soup.prettify())
    assert exp_text == act_text


def test_format_note_with_single_missing_file(td: Data, addon_dir: Path, details_formatter: DetailsFormatter):
    note: Note = td.create_note_without_files()
    td.update_front_field(note, 'Missing file: <img src="absents.png">')
    exp_html: str = f"""
        <h3>Total note size: <code style="font-family:Consolas,monospace">73 B</code></h3>
        <li>Texts size: <code style="font-family:Consolas,monospace">73 B</code></li>
        <li>Files size: <code style="font-family:Consolas,monospace">0 B</code></li>
        <li>Files (big to small):</li>
        <ol>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                absents.png: <code style="font-family:Consolas,monospace">0 B</code>
            </li>
        </ol>
                    """
    soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
    act_text: str = details_formatter.format_note_detailed_text(note)
    exp_text: str = str(soup.prettify())
    assert exp_text == act_text


def test_unrecognized_mime_type(td: Data, addon_dir: Path, details_formatter: DetailsFormatter):
    files: dict[FieldName, dict[MediaFile, FileContent]] = {
        DefaultFields.front_field_name: {
            MediaFile("without_extension"): DefaultFields.content0,
            MediaFile("unrecognized_extension.ae1"): DefaultFields.content1
        }
    }
    note: Note = td.create_note_with_given_files(files)
    exp_html: str = f"""
        <h3> Total note size: <code style="font-family:Consolas,monospace">94 B</code></h3>
        <li> Texts size: <code style="font-family:Consolas,monospace">82 B</code></li>
        <li> Files size: <code style="font-family:Consolas,monospace">12 B</code></li>
        <li> Files (big to small):</li>
        <ol>
            <li style="white-space:nowrap">
                <img alt="Other file"  height="15" src="{addon_dir}/button/icon/other.png" style="vertical-align: middle;"/>
                without_extension: <code style="font-family:Consolas,monospace">7 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Other file" height="15" src="{addon_dir}/button/icon/other.png" style="vertical-align: middle;"/>
                unrecognized_extension.ae1: <code style="font-family:Consolas,monospace">5 B</code>
            </li>
        </ol>
                """
    soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
    act_text: str = details_formatter.format_note_detailed_text(note)
    exp_text: str = str(soup.prettify())
    assert exp_text == act_text


def test_limit_showed_number_of_files(td: Data, addon_dir: Path, details_formatter: DetailsFormatter):
    files: dict[MediaFile, FileContent] = __generate_files(15)
    fields: dict[FieldName, dict[MediaFile, FileContent]] = {
        DefaultFields.front_field_name: files
    }
    note: Note = td.create_note_with_given_files(fields)
    exp_html: str = f"""
        <h3>Total note size:<code style="font-family:Consolas,monospace">523 B</code></h3>
        <li>Texts size:<code style="font-family:Consolas,monospace">373 B</code></li>
        <li>Files size:<code style="font-family:Consolas,monospace">150 B</code></li>
        <li>Files (big to small):</li>
        <ol>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_00.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_01.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_02.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_03.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_04.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_05.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_06.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_07.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_08.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_09.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">More 5 files are hidden</li>
        </ol>
                """
    soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
    act_text: str = details_formatter.format_note_detailed_text(note)
    exp_text: str = str(soup.prettify())
    assert exp_text == act_text


def test_limit_showed_number_of_files_exact(td: Data, addon_dir: Path, details_formatter: DetailsFormatter):
    files: dict[MediaFile, FileContent] = __generate_files(10)
    fields: dict[FieldName, dict[MediaFile, FileContent]] = {
        DefaultFields.front_field_name: files
    }
    note: Note = td.create_note_with_given_files(fields)
    exp_html: str = f"""
        <h3>Total note size:<code style="font-family:Consolas,monospace">353 B</code></h3>
        <li>Texts size:<code style="font-family:Consolas,monospace">253 B</code></li>
        <li>Files size:<code style="font-family:Consolas,monospace">100 B</code></li>
        <li>Files (big to small):</li>
        <ol>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_00.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_01.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_02.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_03.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_04.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_05.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_06.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_07.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_08.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
            <li style="white-space:nowrap">
                <img alt="Image file" height="15" src="{addon_dir}/button/icon/image.png" style="vertical-align: middle;"/>
                file_09.png:<code style="font-family:Consolas,monospace">10 B</code>
            </li>
        </ol>
                """
    soup: BeautifulSoup = BeautifulSoup(exp_html, 'html.parser')
    act_text: str = details_formatter.format_note_detailed_text(note)
    exp_text: str = str(soup.prettify())
    assert exp_text == act_text


def __generate_files(file_number):
    return {MediaFile(f"file_{i:02d}.png"): FileContent(f"content_{i:02d}") for i in range(file_number)}
