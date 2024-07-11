# Features

**Table of content**

- [How note size is calculated](#how-note-size-is-calculated)
- [How collection size is calculated](#how-collection-size-is-calculated)
- [Implemented features](#implemented-features)
    - [In Deck Browser](#in-deck-browser)
    - [In Browser](#in-browser)
    - [In Editor when adding new note](#in-editor-when-adding-new-note)

## How note size is calculated

A note size comprises:

1. Size of texts stored in fields.
2. Sizes of files referred from the fields. File size on the disk is used.

**Some symbols can consume more than 1 byte.**  
For example, a space can consume 6 bytes because it can be represented internally as `&nbsp;`.  
Also, Unicode symbols can consume from 1 to 4 bytes each (`A` consumes 1 byte, while `𝛴` consumes 4 bytes).  
Often Anki automatically wraps your text with HTML tags which consume additional bytes.

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/description/images/calculate_note_size.png)

## How collection size is calculated

Collection size is the size of file `collection.anki2` located in the current profile folder.  
Media size is the size of folder `collection.media` located in the current profile folder.
Total size is sum of the collection and media sizes.

## Implemented features

1. Show collection size in Deck Browser
2. See the note size at the real time as you are editing it.
3. Sort notes by "Size" columns.
4. Show details about a note by clicking the "123KB" button.

### In Deck Browser

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/description/images/collection_size.png)

### In Browser

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/description/images/edit_note.png)

### In Editor when adding new note

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/description/images/add_note.png)
