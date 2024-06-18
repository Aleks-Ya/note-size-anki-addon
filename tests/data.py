from anki.collection import Collection
from anki.notes import Note

from note_size.types import MediaFile


class Data:
    content1: bytes = 'picture'.encode()
    content2: bytes = 'sound'.encode()
    content3: bytes = 'animation'.encode()
    file1: MediaFile = MediaFile('picture.jpg')
    file2: MediaFile = MediaFile('sound.mp3')
    file3: MediaFile = MediaFile('animation.gif')
    front_field_content_with_files: str = f'Files: <img src="{file1}"> <img src="{file2}"> ∑￡'
    back_field_content_with_files: str = f'Files: <img src="{file1}"> <img src="{file3}"> ∆¥'
    front_field_content_without_files: str = 'The field on the front card ∑￡'
    back_field_content_without_files: str = 'Another field on the back card ∆¥'
    front_field_name: str = 'Front'
    back_field_name: str = 'Back'

    def __init__(self, col: Collection):
        self.col: Collection = col

    def create_note_with_files(self) -> Note:
        self._write_data_no_renaming(Data.file1, Data.content1)
        self._write_data_no_renaming(Data.file2, Data.content2)
        self._write_data_no_renaming(Data.file3, Data.content3)
        note: Note = self.col.newNote()
        note[self.front_field_name] = self.front_field_content_with_files
        note[self.back_field_name] = self.back_field_content_with_files
        self.col.addNote(note)
        return note

    def create_note_without_files(self) -> Note:
        note: Note = self.col.newNote()
        note[self.front_field_name] = self.front_field_content_without_files
        note[self.back_field_name] = self.back_field_content_without_files
        self.col.addNote(note)
        return note

    @staticmethod
    def update_front_field(note: Note, content: str) -> None:
        note[Data.front_field_name] = content
        note.col.update_note(note)

    def _write_data_no_renaming(self, file: MediaFile, content: bytes):
        actual: MediaFile = self.col.media.write_data(file, content)
        if actual != file:
            raise RuntimeError(f"File was renamed: original={file}, renamed={actual}")
