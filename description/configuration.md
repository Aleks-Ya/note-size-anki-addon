# "Note Size" addon configuration

**Table of content**

- [Find configuration in Anki](#find-configuration-in-anki)
- [Supported properties](#supported-properties)
    - [Logging](#logging)
        - [Logging Level](#logging-level)
    - [Deck Browser](#deck-browser)
        - [Show Full Collection Size](#show-full-collection-size)
    - [Size Button](#size-button)
        - [Enabled](#enabled)
        - [Max Filename Length](#max-filename-length)
        - [Max Files To Show](#max-files-to-show)
    - [Cache](#cache)
        - [Warmup Enabled](#warmup-enabled)

## Find configuration in Anki

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/description/images/open_config.png)

## Supported properties

### Logging

#### Logging Level

- Property name: `Logging` - `Logger Level`
- Type: String
- Default value: `INFO`
- Possible values: `NOTSET`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

Set the logger level.  
Output log file on Linux: `~/.local/share/Anki2/logs/addons/1188705668/note_size.log`.  
Output log file on Windows: `c:\Users\%USERNAME%\AppData\Roaming\Anki2\logs\addons\1188705668\note_size.log`.

### Deck Browser

#### Show Full Collection Size

- Property name: `Deck Browser` - `Show Full Collection Size`
- Type: Boolean
- Default value: `true`
- Possible values: `true`, `false`

Display or hide the Collection size in the Deck Browser:  
![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/description/images/collection_size.png)

### Size Button

#### Enabled

- Property name: `Size Button` - `Enabled`
- Type: Boolean
- Default value: `true`
- Possible values: `true`, `false`

Display or hide the Size Button in the Browser, in the Editor and in the Adding note window.

#### Max Filename Length

- Property name: `Size Button` - `Details Window` - `Max Filename Length`
- Type: Integer
- Default value: `100`
- Possible values: positive number

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/description/images/config_max_filename_length.png)

#### Max Files To Show

- Property name: `Size Button` - `Details Window` - `Max Files To Show`
- Type: Integer
- Default value: `10`
- Possible values: positive number

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/description/images/config_max_files_to_show.png)

### Cache

#### Warmup Enabled

- Property name: `Cache` - `Warmup Enabled`
- Type: Boolean
- Default value: `true`
- Possible values: `true`, `false`

Sizes of notes are cached in memory to allow the Browser show any number of notes without any delays.  
On Anki startup the cache is populated (warm-up) in a background thread. Warmup takes several seconds depending on
collection size. This doesn't block Anki interface.  
If cache warmup is disabled, the Browser can show notes slower when you search them the first time.  
Cached sizes are individually updated when you edit or add notes.
