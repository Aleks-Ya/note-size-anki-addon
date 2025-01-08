# Changelog for "Note Size" Anki addon

## [v2.5.3](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v2.5.3) - 2025-01-08

1. __[BUG]__ Error when click on Browser Button in cards mode

## [v2.5.2](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v2.5.2) - 2025-01-07

1. __[BUG]__ Size calculator properly handles files used in several notes
2. __[BUG]__ Refresh BrowserButton when clicked
3. __[MISC]__ Profiler does not overwrite previous reports

## [v2.5.1](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v2.5.1) - 2025-01-06

1. __[BUG]__ Do not save caches to file if caches were not initialized
2. __[MISC]__ Read cache file in background
3. __[MISC]__ Set title for progress bar in Details Dialog

## [v2.5.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v2.5.0) - 2025-01-05

1. __[FEATURE]__ Speed up cache initialization
2. __[BUG]__ DeckBrowser uses cache before cache initialization
3. __[BUG]__ "Refresh cache" button does not work when cache warmup is disabled
4. __[MISC]__ Setup GitHub actions

## [v2.4.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v2.4.0) - 2024-10-06

1. __[FEATURE]__ Show size of notes found in Browser
2. __[MISC]__ Setup SonarQube
3. __[MISC]__ Add profiler

## [v2.3.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v2.3.0) - 2024-09-06

1. __[FEATURE]__ New note size details dialog
2. __[FEATURE]__ Speed up cache initialization
3. __[DOCS]__ Extract developer manual
4. __[DOCS]__ Setup auto rendering of table of content in MarkDown
5. __[MISC]__ Migrate to bump-my-version

## [v2.2.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v2.2.0) - 2024-08-11

1. __[FEATURE]__ Display "Unused" and "Trash" collection sizes in Deck Browser
2. __[FEATURE]__ Show cache initialization progress dialog
3. __[FEATURE]__ Add "Info" menu item
4. __[FEATURE]__ Refresh note sizes that were modified during media sync
5. __[FEATURE]__ Display collection size after cache initialization
6. __[FEATURE]__ Set 0 precision for collection size
7. __[FEATURE]__ Refresh note sizes only after media sync finished
8. __[FEATURE]__ Delete cache file after reading on startup
9. __[BUG]__ Ignore cache file reading errors
10. __[BUG]__ Incorrect storing boolean settings
11. __[BUG]__ Reading partially invalid cache file
12. __[BUG]__ Ignore error on saving cache file
13. __[DOCS]__ Migrate from `git-changelog` to manual changelog updates
14. __[DOCS]__ Simplify changelog structure
15. __[DOCS]__ Update documentation
16. __[MISC]__ Set DEBUG default log level
17. __[MISC]__ Reduce size of some long log entries

## [v2.1.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v2.1.0) - 2024-07-29

1. __[FEATURE]__ Update cache when other addons update notes
2. __[FEATURE]__ Store cache on disk on exit

## [v2.0.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v2.0.0) - 2024-07-26

1. __[FEATURE]__ GUI for configuration
2. __[MISC]__ Migrate from UnitTest to PyTest

## [v1.15.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.15.0) - 2024-07-15

1. __[FEATURE]__ Background color of Size button depends on note size
2. __[BUG]__ Fix updating Size button when Add Editor is open
3. __[MISC]__ Add space before size units
4. __[MISC]__ Align size in Browser cells by center
5. __[MISC]__ Install from file to the same folder as from addons catalog

## [v1.14.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.14.0) - 2024-07-11

1. __[MISC]__ Remove prefix "Size:" from the Size button
2. __[MISC]__ Use default font for Browser cells

## [v1.13.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.13.0) - 2024-07-09

1. __[FEATURE]__ Add "Deck Browser - Show Full Collection Size" config property
2. __[FEATURE]__ Add "Size Button - Enabled" config property

## [v1.12.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.12.0) - 2024-07-08

1. __[FEATURE]__ Display Collection size in Deck Browser
2. __[DOCS]__ Split description in several pages
3. __[MISC]__ Upgrade to Anki 24.6.3

## [v1.11.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.11.0) - 2024-06-23

1. __[FEATURE]__ Add "Logger Level" config property
2. __[BUG]__ Fix failed to create log dir #2
3. __[DOCS]__ Add "Configuration" page

## [v1.10.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.10.0) - 2024-06-23

1. __[FEATURE]__ Add changelog
2. __[FEATURE]__ Limit number of files shown in Details window
3. __[BUG]__ Reading config failure after addon updates
4. __[BUG]__ Add "alt" attribute to "img" tags on Details window
5. __[BUG]__ Add "use_cache" parameter to SizeCalculator#()
6. __[BUG]__ Log file cannot be deleted during addon deletion on Windows
7. __[MISC]__ Log response from web.eval

## [v1.9.1](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.9.1) - 2024-06-22

1. __[BUG]__ Fix displaying details about files without extension
2. __[MISC]__ Refactor unit-tests

## [v1.9.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.9.0) - 2024-06-19

1. __[FEATURE]__ Add `Size (texts)` and `Size (files)` columns
2. __[FEATURE]__ Add addon config
3. __[FEATURE]__ Add config parameter "Warmup Enabled"
4. __[FEATURE]__ Include version to name
5. __[MISC]__ Cache file sizes in media folder
6. __[MISC]__ Improve ItemId cache
7. __[MISC]__ Synchronize cache functions
8. __[MISC]__ Refactor unit-tests

## [v1.8.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.8.0) - 2024-06-16

1. __[FEATURE]__ Add icons for file types on details window
2. __[MISC]__ Do not add handler to root logger

## [v1.7.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.7.0) - 2024-06-16

1. __[FEATURE]__ Use "Consolas" font on Windows [#1](https://github.com/Aleks-Ya/note-size-anki-addon/issues/1)
2. __[BUG]__ Exclude `meta.json` from distribution
3. __[DOCS]__ Add link to Anki forum support page
4. __[MISC]__ Add `manifest.json`

## [v1.6.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.6.0) - 2024-06-13

1. __[DOCS]__ Update addon description

## [v1.5.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.5.0) - 2024-06-11

1. __[FEATURE]__ Update Size Button by typing timer
2. __[BUG]__ Calculate text size in UTF-8
3. __[MISC]__ Refactoring

## [v1.4.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.4.0) - 2024-06-11

1. __[FEATURE]__ Show note size during adding new note
2. __[FEATURE]__ Details window works during adding note
3. __[DOCS]__ Add UML class diagram
4. __[MISC]__ Add `deploy_locally.sh`
5. __[MISC]__ Refactoring

## [v1.3.1](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.3.1) - 2024-06-09

1. __[BUG]__ Inactivate the Size Button when adding new note

## [v1.3.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.3.0) - 2024-06-09

1. __[MISC]__ Refactoring

## [v1.2.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.2.0) - 2024-06-09

1. __[FEATURE]__ Add note size caching
2. __[FEATURE]__ Configure cache warmup on startup

## [v1.1.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.1.0) - 2024-06-08

1. __[FEATURE]__ Format size as `<code>`
2. __[BUG]__ Fix size button in adding editor mode

## [v1.0.5](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.0.5) - 2024-06-08

1. __[DOCS]__ Improve documentation
2. __[MISC]__ Refactoring

## [v1.0.4](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.0.4) - 2024-06-07

1. __[FEATURE]__ Show no files in the details window
2. __[FEATURE]__ Sort descending by default
3. __[BUG]__ Exclude "__pycache__" from distribution
4. __[DOCS]__ Improve `description.md`
5. __[MISC]__ Rename log file

## [v1.0.3](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.0.3) - 2024-06-07

1. __[BUG]__ Fix imports

## [v1.0.2](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.0.2) - 2024-06-07

1. __[BUG]__ Give `.ankiaddon` extension to distribution
2. __[DOCS]__ Add addon description
3. __[MISC]__ Store version in `version.txt`

## [v1.0.1](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.0.1) - 2024-06-07

1. __[MISC]__ Configure `bumpversion`

## [v1.0.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.0.0) - 2024-06-07

1. __[FEATURE]__ Implemented size column, size button and details window
2. __[MISC]__ Running unit-tests with Tox
