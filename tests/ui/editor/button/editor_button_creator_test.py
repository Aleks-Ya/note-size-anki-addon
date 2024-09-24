from aqt.editor import Editor

from note_size.ui.editor.button.editor_button_creator import EditorButtonCreator


def test_create_size_button(editor_button_creator: EditorButtonCreator, editor_edit_mode: Editor, editor_add_mode: Editor):
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
