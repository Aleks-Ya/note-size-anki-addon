import pytest
from aqt.editor import Editor

from note_size.ui.editor.button.editor_button_creator import EditorButtonCreator


@pytest.mark.skip_for_beta
@pytest.mark.skip_for_earliest
def test_create_size_button_current(editor_button_creator: EditorButtonCreator, editor_edit_mode: Editor,
                                    editor_add_mode: Editor):
    exp: str = """<button tabindex=-1
                        id=size_button
                        class="anki-addon-button linkb perm"
                        type="button"
                        title="Note size. Click for details"
                        data-cantoggle="0"
                        data-command="size_button_cmd"
                >
                    
                    0 B
                </button>"""
    assert editor_button_creator.create_size_button(editor_edit_mode) == exp
    assert editor_button_creator.create_size_button(editor_add_mode) == exp


@pytest.mark.skip_for_current
@pytest.mark.skip_for_earliest
def test_create_size_button_beta(editor_button_creator: EditorButtonCreator, editor_edit_mode: Editor,
                                 editor_add_mode: Editor):
    exp: str = """<button tabindex=-1
                        id=size_button
                        class="anki-addon-button linkb perm"
                        type="button"
                        title="Note size. Click for details"
                        data-cantoggle="0"
                        data-command="size_button_cmd"
                >
                    
                    0 B
                </button>"""
    assert editor_button_creator.create_size_button(editor_edit_mode) == exp
    assert editor_button_creator.create_size_button(editor_add_mode) == exp


@pytest.mark.skip_for_beta
@pytest.mark.skip_for_current
def test_create_size_button_earliest(editor_button_creator: EditorButtonCreator, editor_edit_mode: Editor,
                                     editor_add_mode: Editor):
    exp: str = """<button tabindex=-1
                        id=size_button
                        class="linkb perm"
                        type="button"
                        title="Note size. Click for details"
                        onclick="pycmd('size_button_cmd');return false;"
                        onmousedown="window.event.preventDefault();"
                >
                    
                    0 B
                </button>"""
    assert editor_button_creator.create_size_button(editor_edit_mode) == exp
    assert editor_button_creator.create_size_button(editor_add_mode) == exp
