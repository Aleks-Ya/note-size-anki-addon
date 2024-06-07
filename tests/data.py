from anki.collection import Collection
from anki.notes import Note


class TestData:
    content1: bytes = b'picture'
    content2: bytes = b'sound'
    content3: bytes = b'animation'
    filename1: str
    filename2: str
    filename3: str
    front_field_content: str
    back_field_content: str
    front_field_name: str = 'Front'
    back_field_name: str = 'Back'

    def create_note(self, col: Collection) -> Note:
        self.filename1: str = col.media.write_data('picture.jpg', self.content1)
        self.filename2: str = col.media.write_data('sound.mp3', self.content2)
        self.filename3: str = col.media.write_data('animation.gif', self.content3)
        note: Note = col.newNote()
        self.front_field_content: str = f'Files: <img src="{self.filename1}"> <img src="{self.filename2}">'
        self.back_field_content: str = f'Files: <img src="{self.filename1}"> <img src="{self.filename3}">'
        note[self.front_field_name] = self.front_field_content
        note[self.back_field_name] = self.back_field_content
        col.addNote(note)
        return note
