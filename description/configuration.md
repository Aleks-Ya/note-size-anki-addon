# "Note Size" addon configuration

## Find configuration in Anki

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/description/open_config.png)

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

### Size Button

#### Max Filename Length

- Property name: `Size Button` - `Details Window` - `Max Filename Length`
- Type: Integer
- Default value: `100`
- Possible values: positive number

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/description/config_max_filename_length.png)

#### Max Files To Show

- Property name: `Size Button` - `Details Window` - `Max Files To Show`
- Type: Integer
- Default value: `10`
- Possible values: positive number

![](https://raw.githubusercontent.com/Aleks-Ya/note-size-anki-addon/main/description/config_max_files_to_show.png)

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
