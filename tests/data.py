from pathlib import Path
from typing import Any

from anki.cards import Card
from anki.decks import DeckId
from anki.models import NoteType
from anki.notes import Note
from aqt import gui_hooks

from note_size.common.collection_holder import CollectionHolder
from note_size.config.config import Config
from note_size.common.types import MediaFile, FieldName, FieldContent, FileContent, SignificantDigits


class MediaFiles:
    picture: MediaFile = MediaFile('picture.jpg')
    sound: MediaFile = MediaFile('sound.mp3')
    animation: MediaFile = MediaFile('animation.gif')
    image: MediaFile = MediaFile('image.png')
    movie: MediaFile = MediaFile('movie.mp4')
    photo: MediaFile = MediaFile('photo.tiff')
    video: MediaFile = MediaFile('video.mov')


class FileContents:
    picture: FileContent = FileContent('picture')
    sound: FileContent = FileContent('sound')
    animation: FileContent = FileContent('animation')


class DefaultFields:
    front_field_name: FieldName = FieldName('Front')
    back_field_name: FieldName = FieldName('Back')
    front_field_content: FieldContent = FieldContent(
        f'Files ∑￡: <img src="{MediaFiles.picture}"> <img src="{MediaFiles.sound}">')
    back_field_content: FieldContent = FieldContent(
        f'Files ∑￡: <img src="{MediaFiles.picture}"> <img src="{MediaFiles.animation}">')
    front_field_content_2: FieldContent = FieldContent('The field on the front card ∑￡')
    back_field_content_2: FieldContent = FieldContent('Another field on the back card ∆¥')


class Digits:
    zero: SignificantDigits = SignificantDigits(0)
    one: SignificantDigits = SignificantDigits(1)
    two: SignificantDigits = SignificantDigits(2)
    three: SignificantDigits = SignificantDigits(3)


class Data:

    def __init__(self, collection_holder: CollectionHolder, module_dir: Path):
        self.__collection_holder: CollectionHolder = collection_holder
        self.note_type: NoteType = self.__collection_holder.col().models.by_name('Basic')
        self.deck_id: DeckId = self.__collection_holder.col().decks.get_current_id()
        self.config_json: Path = module_dir.joinpath("config.json")

    def create_note_with_files(self) -> Note:
        note: Note = self.create_note_with_given_files({
            DefaultFields.front_field_name: {
                MediaFiles.picture: FileContents.picture,
                MediaFiles.sound: FileContents.sound
            },
            DefaultFields.back_field_name: {
                MediaFiles.picture: FileContents.picture,
                MediaFiles.animation: FileContents.animation
            }
        })
        return note

    def create_note_with_given_fields(self,
                                      front_field_content: str = "Front content",
                                      back_field_content: str = "Back content",
                                      new_note: bool = False) -> Note:
        front_field_content: FieldContent = FieldContent(front_field_content)
        back_field_content: FieldContent = FieldContent(back_field_content)
        note: Note = self.__collection_holder.col().new_note(self.note_type)
        note[DefaultFields.front_field_name] = front_field_content
        note[DefaultFields.back_field_name] = back_field_content
        if not new_note:
            self.__collection_holder.col().add_note(note, self.deck_id)
        gui_hooks.add_cards_did_add_note(note)
        return note

    def create_note_without_files(self, new_note: bool = False) -> Note:
        return self.create_note_with_given_fields(DefaultFields.front_field_content_2,
                                                  DefaultFields.back_field_content_2,
                                                  new_note)

    def create_note_with_given_files(self, fields: dict[FieldName, dict[MediaFile, FileContent]]) -> Note:
        note: Note = self.__collection_holder.col().new_note(self.note_type)
        field_contents: dict[FieldName, FieldContent] = {field_name: self.__add_files_to_field(field_files)
                                                         for field_name, field_files in fields.items()}
        for field_name, field_content in field_contents.items():
            note[field_name] = field_content
        self.__collection_holder.col().add_note(note, self.deck_id)
        gui_hooks.add_cards_did_add_note(note)
        return note

    def write_file(self, media_file: MediaFile, file_content: str) -> None:
        full_path: Path = Path(self.__collection_holder.col().media.dir()).joinpath(media_file)
        full_path.write_text(file_content)

    @staticmethod
    def update_front_field(note: Note, content: str) -> None:
        note[DefaultFields.front_field_name] = content
        note.col.update_note(note)

    @staticmethod
    def append_front_field(note: Note, content: str) -> None:
        old_content: str = note[DefaultFields.front_field_name]
        new_content: str = old_content + content
        Data.update_front_field(note, new_content)

    @staticmethod
    def replace_in_front_field(note: Note, old: str, new: str) -> None:
        current_content: str = note[DefaultFields.front_field_name]
        replaced_content: str = current_content.replace(old, new)
        note[DefaultFields.front_field_name] = replaced_content
        note.col.update_note(note)

    def read_config(self) -> Config:
        return Config.from_path(self.config_json)

    def read_config_updated(self, overwrites: dict[str, Any]) -> Config:
        return Config.from_path_updated(self.config_json, overwrites)

    def create_card_with_files(self) -> Card:
        note: Note = self.create_note_with_files()
        return note.cards()[0]

    def create_card_without_files(self, new_note: bool = False) -> Card:
        note: Note = self.create_note_without_files(new_note)
        return note.cards()[0]

    def __add_files_to_field(self, files: dict[MediaFile, FileContent]) -> FieldContent:
        field_content: FieldContent = FieldContent("Files ∑￡:")
        for media_file, file_content in files.items():
            media_file: MediaFile = self.__collection_holder.col().media.write_data(media_file, file_content.encode())
            field_content += f' <img src="{media_file}">'
        return field_content
