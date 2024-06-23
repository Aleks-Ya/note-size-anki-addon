# Features

## How note size is calculated

A note size comprises:

1. Size of texts stored in fields.
2. Sizes of files referred from the fields. File size on the disk is used.

**Some symbols can consume more than 1 byte.**  
For example, a space can consume 6 bytes because it can be represented internally as `&nbsp;`.  
Also, Unicode symbols can consume from 1 to 4 bytes each (`A` consumes 1 byte, while `𝛴` consumes 4 bytes).  
Often Anki automatically wraps your text with HTML tags which consume additional bytes.

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/description/calculate_note_size.png)

## Implemented features

1. See the note size at the real time as you are editing it.
2. Sort notes by "Size" columns.
3. Show details about a note by clicking the "Size: 1KB" button.

### In Browser

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/description/edit_note.png)

### In Editor when adding new note

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/description/add_note.png)
