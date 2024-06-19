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
        content1: bytes = 'picture'.encode()
        content2: bytes = 'sound'.encode()
        content3: bytes = 'animation'.encode()
        file1: MediaFile = MediaFile('picture.jpg')
        file2: MediaFile = MediaFile('sound.mp3')
        file3: MediaFile = MediaFile('animation.gif')
        front_field_content_with_files: str = f'Files: <img src="{file1}"> <img src="{file2}"> ∑￡'
        back_field_content_with_files: str = f'Files: <img src="{file1}"> <img src="{file3}"> ∆¥'
        self.__write_data_no_renaming(file1, content1)
        self.__write_data_no_renaming(file2, content2)
        self.__write_data_no_renaming(file3, content3)
        note: Note = self.col.newNote()
        note[self.__front_field_name] = front_field_content_with_files
        note[self.__back_field_name] = back_field_content_with_files
        self.col.addNote(note)
        file_contents: list[bytes] = [content1, content2, content3]
        files: list[MediaFile] = [file1, file2, file3]
        return NoteData(note, file_contents, files,
                        Data.__front_field_name, Data.__back_field_name,
                        front_field_content_with_files,
                        back_field_content_with_files)

    def create_note_without_files(self) -> NoteData:
        front_field_content_without_files: str = 'The field on the front card ∑￡'
        back_field_content_without_files: str = 'Another field on the back card ∆¥'
        note: Note = self.col.newNote()
        note[self.__front_field_name] = front_field_content_without_files
        note[self.__back_field_name] = back_field_content_without_files
        self.col.addNote(note)
        return NoteData(note, [], [],
                        Data.__front_field_name, Data.__back_field_name,
                        front_field_content_without_files,
                        back_field_content_without_files)

    @staticmethod
    def update_front_field(note: Note, content: str) -> None:
        note[Data.__front_field_name] = content
        note.col.update_note(note)

    def __write_data_no_renaming(self, file: MediaFile, content: bytes):
        actual: MediaFile = self.col.media.write_data(file, content)
        if actual != file:
            raise RuntimeError(f"File was renamed: original={file}, renamed={actual}")

    @staticmethod
    def read_config() -> Config:
        config_json: Path = Path(__file__).parent.parent.joinpath("note_size").joinpath("config.json")
        return Config.from_path(config_json)
