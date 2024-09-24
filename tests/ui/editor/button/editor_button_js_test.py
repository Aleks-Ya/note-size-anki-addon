from anki.notes import Note

from note_size.ui.editor.button.editor_button_js import EditorButtonJs
from tests.data import Data


def test_show_size_button_js_edit_mode(editor_button_js: EditorButtonJs, td: Data):
    note: Note = td.create_note_with_files()
    add_mode: bool = False
    js: str = editor_button_js.show_size_button_js(note, add_mode)
    assert js == """
            try {
                const sizeButton = document.getElementById('size_button');
                if (sizeButton) {
                    sizeButton.style.display = 'block';
                    sizeButton.textContent = '143 B';
                    sizeButton.style.backgroundColor = 'PaleGreen';
                }
            } catch (error) {
              error.stack
            } """


def test_show_size_button_js_add_mode(editor_button_js: EditorButtonJs, td: Data):
    note: Note = td.create_note_with_files()
    add_mode: bool = True
    js: str = editor_button_js.show_size_button_js(note, add_mode)
    assert js == """
            try {
                const sizeButton = document.getElementById('size_button');
                if (sizeButton) {
                    sizeButton.style.display = 'block';
                    sizeButton.textContent = '143 B';
                    sizeButton.style.backgroundColor = 'PaleGreen';
                }
            } catch (error) {
              error.stack
            } """


def test_show_size_button_js_no_note(editor_button_js: EditorButtonJs, td: Data):
    js: str = editor_button_js.show_size_button_js(None, None)
    assert js == """
            try {
                const sizeButton = document.getElementById('size_button');
                if (sizeButton) {
                    sizeButton.style.display = 'block';
                    sizeButton.textContent = '0 B';
                    sizeButton.style.backgroundColor = 'PaleGreen';
                }
            } catch (error) {
              error.stack
            } """


def test_hide_size_button_js(editor_button_js: EditorButtonJs, td: Data):
    js: str = editor_button_js.hide_size_button_js()
    assert js == """
            try {
                const sizeButton = document.getElementById('size_button');
                if (sizeButton) {
                    sizeButton.style.display = 'none';
                }
            } catch (error) {
              error.stack
            } """
