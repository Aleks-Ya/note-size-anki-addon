from pathlib import Path

from anki.collection import Collection
from anki.notes import Note

from note_size import Config
from note_size.types import MediaFile, FieldName, FieldContent, FileContent


class DefaultFields:
    content0: FileContent = FileContent('picture')
    content1: FileContent = FileContent('sound')
    content2: FileContent = FileContent('animation')
    file0: MediaFile = MediaFile('picture.jpg')
    file1: MediaFile = MediaFile('sound.mp3')
    file2: MediaFile = MediaFile('animation.gif')
    front_field_name: FieldName = FieldName('Front')
    back_field_name: FieldName = FieldName('Back')
    front_field_content: FieldContent = FieldContent(f'Files ∑￡: <img src="{file0}"> <img src="{file1}">')
    back_field_content: FieldContent = FieldContent(f'Files ∑￡: <img src="{file0}"> <img src="{file2}">')


class Data:

    def __init__(self, col: Collection):
        self.col: Collection = col

    def create_note_with_files(self) -> Note:
        note: Note = self.create_note_with_given_files({
            DefaultFields.front_field_name: {
                DefaultFields.file0: DefaultFields.content0,
                DefaultFields.file1: DefaultFields.content1
            },
            DefaultFields.back_field_name: {
                DefaultFields.file0: DefaultFields.content0,
                DefaultFields.file2: DefaultFields.content2
            }
        })
        return note

    def create_note_without_files(self) -> Note:
        front_field_content: FieldContent = FieldContent('The field on the front card ∑￡')
        back_field_content: FieldContent = FieldContent('Another field on the back card ∆¥')
        note: Note = self.col.newNote()
        note[DefaultFields.front_field_name] = front_field_content
        note[DefaultFields.back_field_name] = back_field_content
        self.col.addNote(note)
        return note

    def create_note_with_given_files(self, fields: dict[FieldName, dict[MediaFile, FileContent]]) -> Note:
        note: Note = self.col.newNote()
        field_contents: dict[FieldName, FieldContent] = {field_name: self.__add_files_to_field(field_files)
                                                         for field_name, field_files in fields.items()}
        for field_name, field_content in field_contents.items():
            note[field_name] = field_content
        self.col.addNote(note)
        return note

    def __add_files_to_field(self, files: dict[MediaFile, FileContent]) -> FieldContent:
        field_content: FieldContent = FieldContent("Files ∑￡:")
        for media_file, file_content in files.items():
            media_file: MediaFile = self.col.media.write_data(media_file, file_content.encode())
            field_content += f' <img src="{media_file}">'
        return field_content

    @staticmethod
    def update_front_field(note: Note, content: str) -> None:
        note[DefaultFields.front_field_name] = content
        note.col.update_note(note)

    @staticmethod
    def read_config() -> Config:
        config_json: Path = Path(__file__).parent.parent.joinpath("note_size").joinpath("config.json")
        return Config.from_path(config_json)
