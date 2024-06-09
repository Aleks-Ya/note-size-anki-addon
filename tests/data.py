from anki.collection import Collection
from anki.notes import Note

from note_size.size_calculator import MediaFile


class TestData:
    content1: bytes = b'picture'
    content2: bytes = b'sound'
    content3: bytes = b'animation'
    filename1: MediaFile
    filename2: MediaFile
    filename3: MediaFile
    front_field_content_with_files: str
    back_field_content_with_files: str
    front_field_content_without_files: str = 'The field on the front card'
    back_field_content_without_files: str = 'Another field on the back card'
    front_field_name: str = 'Front'
    back_field_name: str = 'Back'

    def create_note_with_files(self, col: Collection) -> Note:
        self.filename1: MediaFile = col.media.write_data('picture.jpg', self.content1)
        self.filename2: MediaFile = col.media.write_data('sound.mp3', self.content2)
        self.filename3: MediaFile = col.media.write_data('animation.gif', self.content3)
        note: Note = col.newNote()
        self.front_field_content_with_files: str = f'Files: <img src="{self.filename1}"> <img src="{self.filename2}">'
        self.back_field_content_with_files: str = f'Files: <img src="{self.filename1}"> <img src="{self.filename3}">'
        note[self.front_field_name] = self.front_field_content_with_files
        note[self.back_field_name] = self.back_field_content_with_files
        col.addNote(note)
        return note

    def create_note_without_files(self, col: Collection) -> Note:
        note: Note = col.newNote()
        note[self.front_field_name] = self.front_field_content_without_files
        note[self.back_field_name] = self.back_field_content_without_files
        col.addNote(note)
        return note
