from ...common.types import MediaFile, FileSize


class DetailsModel:
    total_note_size_text: str
    texts_note_size_text: str
    files_note_size_text: str
    file_sizes: dict[MediaFile, FileSize]
