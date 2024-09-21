from aqt.editor import Editor

from note_size.ui.editor.button.button_creator import ButtonCreator


def test_create_size_button(button_creator: ButtonCreator, editor_edit_mode: Editor, editor_add_mode: Editor):
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
    assert button_creator.create_size_button(editor_edit_mode) == exp
    assert button_creator.create_size_button(editor_add_mode) == exp
