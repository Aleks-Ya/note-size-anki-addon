from pathlib import Path

from anki.collection import Collection
from anki.notes import Note

from note_size import Config
from note_size.types import MediaFile


class NoteData:

    def __init__(self, note: Note, file_contents: list[bytes], files: list[MediaFile],
                 front_field_name: str, back_field_name: str,
                 front_field_content: str, back_field_content: str):
        self.note: Note = note
        self.file_contents: list[bytes] = file_contents
        self.files: list[MediaFile] = files
        self.front_field_content: str = front_field_content
        self.back_field_content: str = back_field_content
        self.front_field_name: str = front_field_name
        self.back_field_name: str = back_field_name


class Data:
    __front_field_name: str = 'Front'
    __back_field_name: str = 'Back'

    def __init__(self, col: Collection):
        self.col: Collection = col

    def create_note_with_files(self) -> NoteData:
        content0: bytes = 'picture'.encode()
        content1: bytes = 'sound'.encode()
        content2: bytes = 'animation'.encode()
        file0: MediaFile = self.col.media.write_data('picture.jpg', content0)
        file1: MediaFile = self.col.media.write_data('sound.mp3', content1)
        file2: MediaFile = self.col.media.write_data('animation.gif', content2)
        front_field_content: str = f'Files: <img src="{file0}"> <img src="{file1}"> ∑￡'
        back_field_content: str = f'Files: <img src="{file0}"> <img src="{file2}"> ∆¥'
        note: Note = self.col.newNote()
        note[self.__front_field_name] = front_field_content
        note[self.__back_field_name] = back_field_content
        self.col.addNote(note)
        file_contents: list[bytes] = [content0, content1, content2]
        files: list[MediaFile] = [file0, file1, file2]
        return NoteData(note, file_contents, files,
                        Data.__front_field_name, Data.__back_field_name,
                        front_field_content, back_field_content)

    def create_note_without_files(self) -> NoteData:
        front_field_content: str = 'The field on the front card ∑￡'
        back_field_content: str = 'Another field on the back card ∆¥'
        note: Note = self.col.newNote()
        note[self.__front_field_name] = front_field_content
        note[self.__back_field_name] = back_field_content
        self.col.addNote(note)
        return NoteData(note, [], [],
                        Data.__front_field_name, Data.__back_field_name,
                        front_field_content, back_field_content)

    @staticmethod
    def update_front_field(note: Note, content: str) -> None:
        note[Data.__front_field_name] = content
        note.col.update_note(note)

    @staticmethod
    def read_config() -> Config:
        config_json: Path = Path(__file__).parent.parent.joinpath("note_size").joinpath("config.json")
        return Config.from_path(config_json)
