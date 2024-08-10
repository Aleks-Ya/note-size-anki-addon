# Changelog for "Note Size" Anki addon

## [v2.1.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v2.1.0) - 2024-07-29

<small>[Compare with v2.0.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v2.0.0...v2.1.0)</small>

1. __[FEATURE]__ Update cache when other addons update notes
2. __[FEATURE]__ Store cache on disk on exit

## [v2.0.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v2.0.0) - 2024-07-26

<small>[Compare with v1.15.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.15.0...v2.0.0)</small>

1. __[FEATURE]__ GUI for configuration
2. __[MISC]__ Migrate from UnitTest to PyTest

## [v1.15.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.15.0) - 2024-07-15

<small>[Compare with v1.14.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.14.0...v1.15.0)</small>

1. __[FEATURE]__ Background color of Size button depends on note size
2. __[BUG]__ Fix updating Size button when Add Editor is open
3. __[MISC]__ Add space before size units
4. __[MISC]__ Align size in Browser cells by center
5. __[MISC]__ Install from file to the same folder as from addons catalog

## [v1.14.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.14.0) - 2024-07-11

<small>[Compare with v1.13.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.13.0...v1.14.0)</small>

1. __[MISC]__ Remove prefix "Size:" from the Size button
2. __[MISC]__ Use default font for Browser cells

## [v1.13.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.13.0) - 2024-07-09

<small>[Compare with v1.12.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.12.0...v1.13.0)</small>

1. __[FEATURE]__ Add "Deck Browser - Show Full Collection Size" config property
2. __[FEATURE]__ Add "Size Button - Enabled" config property

## [v1.12.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.12.0) - 2024-07-08

<small>[Compare with v1.11.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.11.0...v1.12.0)</small>

1. __[FEATURE]__ Display Collection size in Deck Browser
2. __[DOCS]__ Split description in several pages
3. __[MISC]__ Upgrade to Anki 24.6.3

## [v1.11.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.11.0) - 2024-06-23

<small>[Compare with v1.10.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.10.0...v1.11.0)</small>

1. __[FEATURE]__ Add "Logger Level" config property
2. __[BUG]__ Fix failed to create log dir #2
3. __[DOCS]__ Add "Configuration" page

## [v1.10.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.10.0) - 2024-06-23

<small>[Compare with v1.9.1](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.9.1...v1.10.0)</small>

1. __[FEATURE]__ Add changelog
2. __[FEATURE]__ Limit number of files shown in Details window
3. __[BUG]__ Reading config failure after addon updates
4. __[BUG]__ Add "alt" attribute to "img" tags on Details window
5. __[BUG]__ Add "use_cache" parameter to SizeCalculator#()
6. __[BUG]__ Log file cannot be deleted during addon deletion on Windows
7. __[MISC]__ Log response from web.eval

## [v1.9.1](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.9.1) - 2024-06-22

<small>[Compare with v1.9.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.9.0...v1.9.1)</small>

1. __[BUG]__ Fix displaying details about files without extension
2. __[MISC]__ Refactor unit-tests

## [v1.9.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.9.0) - 2024-06-19

<small>[Compare with v1.8.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.8.0...v1.9.0)</small>

1. __[FEATURE]__ Add `Size (texts)` and `Size (files)` columns
2. __[FEATURE]__ Add addon config
3. __[FEATURE]__ Add config parameter "Warmup Enabled"
4. __[FEATURE]__ Include version to name
5. __[MISC]__ Cache file sizes in media folder
6. __[MISC]__ Improve ItemId cache
7. __[MISC]__ Synchronize cache functions
8. __[MISC]__ Refactor unit-tests

## [v1.8.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.8.0) - 2024-06-16

<small>[Compare with v1.7.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.7.0...v1.8.0)</small>

1. __[FEATURE]__ Add icons for file types on details window
2. __[MISC]__ Do not add handler to root logger

## [v1.7.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.7.0) - 2024-06-16

<small>[Compare with v1.6.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.6.0...v1.7.0)</small>

1. __[FEATURE]__ Use "Consolas" font on Windows [#1](https://github.com/Aleks-Ya/note-size-anki-addon/issues/1)
2. __[BUG]__ Exclude `meta.json` from distribution
3. __[DOCS]__ Add link to Anki forum support page
4. __[MISC]__ Add `manifest.json`

## [v1.6.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.6.0) - 2024-06-13

<small>[Compare with v1.5.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.5.0...v1.6.0)</small>

1. __[DOCS]__ Update addon description

## [v1.5.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.5.0) - 2024-06-11

<small>[Compare with v1.4.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.4.0...v1.5.0)</small>

1. __[FEATURE]__ Update Size Button by typing timer
2. __[BUG]__ Calculate text size in UTF-8
3. __[MISC]__ Refactoring

## [v1.4.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.4.0) - 2024-06-11

<small>[Compare with v1.3.1](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.3.1...v1.4.0)</small>

1. __[FEATURE]__ Show note size during adding new note
2. __[FEATURE]__ Details window works during adding note
3. __[DOCS]__ Add UML class diagram
4. __[MISC]__ Add `deploy_locally.sh`
5. __[MISC]__ Refactoring

## [v1.3.1](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.3.1) - 2024-06-09

<small>[Compare with v1.3.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.3.0...v1.3.1)</small>

1. __[BUG]__ Inactivate the Size Button when adding new note

## [v1.3.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.3.0) - 2024-06-09

<small>[Compare with v1.2.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.2.0...v1.3.0)</small>

1. __[MISC]__ Refactoring

## [v1.2.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.2.0) - 2024-06-09

<small>[Compare with v1.1.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.1.0...v1.2.0)</small>

1. __[FEATURE]__ Add note size caching
2. __[FEATURE]__ Configure cache warmup on startup

## [v1.1.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.1.0) - 2024-06-08

<small>[Compare with v1.0.5](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.0.5...v1.1.0)</small>

1. __[FEATURE]__ Format size as `<code>`
2. __[BUG]__ Fix size button in adding editor mode

## [v1.0.5](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.0.5) - 2024-06-08

<small>[Compare with v1.0.4](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.0.4...v1.0.5)</small>

1. __[DOCS]__ Improve documentation
2. __[MISC]__ Refactoring

## [v1.0.4](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.0.4) - 2024-06-07

<small>[Compare with v1.0.3](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.0.3...v1.0.4)</small>

1. __[FEATURE]__ Show no files in the details window
2. __[FEATURE]__ Sort descending by default
3. __[BUG]__ Exclude "__pycache__" from distribution
4. __[DOCS]__ Improve `description.md`
5. __[MISC]__ Rename log file

## [v1.0.3](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.0.3) - 2024-06-07

<small>[Compare with v1.0.2](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.0.2...v1.0.3)</small>

1. __[BUG]__ Fix imports

## [v1.0.2](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.0.2) - 2024-06-07

<small>[Compare with v1.0.1](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.0.1...v1.0.2)</small>

1. __[BUG]__ Give `.ankiaddon` extension to distribution
2. __[DOCS]__ Add addon description
3. __[MISC]__ Store version in `version.txt`

## [v1.0.1](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.0.1) - 2024-06-07

<small>[Compare with v1.0.0](https://github.com/Aleks-Ya/note-size-anki-addon/compare/v1.0.0...v1.0.1)</small>

1. __[MISC]__ Configure `bumpversion`

## [v1.0.0](https://github.com/Aleks-Ya/note-size-anki-addon/releases/tag/v1.0.0) - 2024-06-07

<small>[Compare with first commit](https://github.com/Aleks-Ya/note-size-anki-addon/compare/f34ecd55addeb54de1714932d1c2c9c964dad6e2...v1.0.0)</small>

1. __[FEATURE]__ Implemented size column, size button and details window
2. __[MISC]__ Running unit-tests with Tox
