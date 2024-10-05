# "Note Size" addon configuration

**Table of content**

<!--TOC-->

- [Open configuration in Anki interface](#open-configuration-in-anki-interface)
- [Supported properties](#supported-properties)
  - [Default values](#default-values)
  - [Deck Browser](#deck-browser)
    - [Show Collection Size](#show-collection-size)
  - [Browser](#browser)
    - [Show size of notes found in Browser](#show-size-of-notes-found-in-browser)
  - [Size Button](#size-button)
    - [Enabled](#enabled)
    - [Color - Enabled](#color---enabled)
    - [Color - Levels](#color---levels)
  - [Logging](#logging)
  - [Cache](#cache)
    - [Enable cache warm-up](#enable-cache-warm-up)
    - [Store cache in file on exit](#store-cache-in-file-on-exit)
    - [Refresh cache](#refresh-cache)

<!--TOC-->

---

## Open configuration in Anki interface

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/docs/images/open-config.png)

---

## Supported properties

### Default values

Default values for all supported properties:
[link](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/note_size/config.json)

Click "Restore Defaults" button to reset all properties to default values:  
![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/docs/images/config-deck-browser.png)

---

### Deck Browser

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/docs/images/config-deck-browser.png)

#### Show Collection Size

Display or hide the Collection size in the Deck Browser:  
![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/docs/images/collection-size.png)

---

### Browser

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/docs/images/config-browser.png)

#### Show size of notes found in Browser

Display or hide the size of all notes found in the Browser:  
![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/docs/images/notes-size.png)

### Size Button

#### Enabled

Display or hide the Size Button in the Browser, in the Editor and in the Adding note window.

---

#### Color - Enabled

Enable or disable marking big notes with color in the Size button.  
Enabled: ![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/docs/images/red-size-button.png)  
Disabled: ![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/docs/images/size-button-color-disabled.png)
---

#### Color - Levels

Configure background colors for the Size button.  
By default, the button background can be painted in 3 colors:

1. Notes having size _less than 100 KB_ are painted green
2. Notes of size _between 100 KB and 1 MB_ are painted orange
3. Notes over _1 MB_ are painted red

---

### Logging

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/docs/images/config-logging.png)

---

### Cache

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/docs/images/config-cache.png)

#### Enable cache warm-up

Sizes of notes are cached in memory to allow the Browser show any number of notes without any delays.  
On Anki startup the cache is populated (warm-up) in a background thread. Warmup takes several seconds depending on
collection size. This doesn't block Anki interface.  
If cache warmup is disabled, the Browser can show notes slower when you search them the first time.  
Cached sizes are individually updated when you edit or add notes.

#### Store cache in file on exit

Sizes of notes are cached in memory to allow the Browser show any number of notes without any delays.  
On Anki startup, the in-memory cache is populated with all existing notes ("warmup").  
Cache populating can take several seconds depending on the collection size.
It's possible to eliminate this delay, if cache is stored on disk when Anki closing.  
If this option is enabled:

- On Anki closing, the in-memory cache can be stored to a file.
- On Anki startup, the cache is read from the file. It eliminates the delay on cache populating.

#### Refresh cache

Clean and rebuild the cache.

---
