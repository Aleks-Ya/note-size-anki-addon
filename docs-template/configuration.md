# "Note Size" addon configuration

**Table of content**

<!--TOC-->

---

## Open configuration in Anki interface

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/docs/images/open_config.png)

---

## Supported properties

### Default values

Default values for all supported properties:
[link](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/note_size/config.json)

---

### Logging

#### Logging Level

Set the logger level.  
Output log file on Linux: `~/.local/share/Anki2/logs/addons/1188705668/note_size.log`.  
Output log file on Windows: `c:\Users\%USERNAME%\AppData\Roaming\Anki2\logs\addons\1188705668\note_size.log`.

- Property name: `Logging` - `Logger Level`
- Type: String
- Default value: `INFO`
- Possible values: `NOTSET`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

---

### Deck Browser

#### Show Collection Size

Display or hide the Collection size in the Deck Browser:  
![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/docs/images/collection_size.png)

- Property name: `Deck Browser` - `Show Collection Size`
- Type: Boolean
- Default value: `true`
- Possible values: `true` or `false`

---

### Size Button

#### Enabled

Display or hide the Size Button in the Browser, in the Editor and in the Adding note window.

- Property name: `Size Button` - `Enabled`
- Type: Boolean
- Default value: `true`
- Possible values: `true` or `false`

---

#### Color - Enabled

Enable or disable marking big notes with color in the Size button.  
Enabled: ![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/docs/images/red_size_button.png)  
Disabled: ![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/docs/images/size_button_color_disabled.png)

- Property name: `Size Button` - `Color` - `Enabled`
- Type: Boolean
- Default value: `true`
- Possible values: `true` or `false`

---

#### Color - Levels

Configure background colors for the Size button.  
By default, the button background can be painted in 3 colors:

1. Notes having size _less than 100 KB_ are painted green
2. Notes of size _between 100 KB and 1 MB_ are painted orange
3. Notes over _1 MB_ are painted red


- Property name: `Size Button` - `Color` - `Levels`
- Type: List of level objects
- Default value: Green: <100 KB, Chocolate: 100 KB - 1 MB, Red: >1 MB
- Possible values:
    - `Levels`: array of one or more levels:
        - `Color`: string with name of any HTML color
        - `Max Size`: string in format `"123 KB"` or `null` for infinity

---

### Cache

#### Warmup Enabled

Sizes of notes are cached in memory to allow the Browser show any number of notes without any delays.  
On Anki startup the cache is populated (warm-up) in a background thread. Warmup takes several seconds depending on
collection size. This doesn't block Anki interface.  
If cache warmup is disabled, the Browser can show notes slower when you search them the first time.  
Cached sizes are individually updated when you edit or add notes.

- Property name: `Cache` - `Warmup Enabled`
- Type: Boolean
- Default value: `true`
- Possible values: `true` or `false`

#### Store cache on disk

Sizes of notes are cached in memory to allow the Browser show any number of notes without any delays.  
On Anki startup, the in-memory cache is populated with all existing notes ("warmup").  
Cache populating can take several seconds depending on the collection size.
It's possible to eliminate this delay, if cache is stored on disk when Anki closing.  
If this option is enabled:

- On Anki closing, the in-memory cache can be stored to a file.
- On Anki startup, the cache is read from the file. It eliminates the delay on cache populating.


- Default value: `true`

---
