import os

from anki.notes import Note, NoteId


class SizeCalculator:
    size_cache: dict[NoteId, int] = {}

    def calculate_note_size(self, note: Note, use_cache: bool = False) -> int:
        if use_cache and note.id in self.size_cache:
            return self.size_cache[note.id]
        else:
            return self._recalculate_total_size(note)

    def _recalculate_total_size(self, note: Note) -> int:
        total_size: int = SizeCalculator.total_text_size(note) + SizeCalculator.total_file_size(note)
        self.size_cache[note.id] = total_size
        return total_size

    @staticmethod
    def total_text_size(note: Note) -> int:
        return sum([len(field) for field in note.fields])

    @staticmethod
    def total_file_size(note: Note) -> int:
        return sum([size for size in SizeCalculator.file_sizes(note).values()])

    @staticmethod
    def file_sizes(note: Note) -> dict[str, int]:
        all_files: dict[str, int] = dict[str, int]()
        for field in note.fields:
            files: list[str] = note.col.media.files_in_str(note.mid, field)
            sizes = {file: os.path.getsize(os.path.join(note.col.media.dir(), file)) for file in files}
            all_files.update(sizes)
        return all_files

    @staticmethod
    def sort_by_size_desc(file_sizes: dict[str, int]) -> dict[str, int]:
        return dict(sorted(file_sizes.items(), key=lambda item: item[1], reverse=True))
