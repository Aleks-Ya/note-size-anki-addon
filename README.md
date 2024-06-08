# Note Size Anki addon

## Description

See [Addon Description](description/description.md)

## Logs

`Tools` -> `Add-ons` -> `Note Size - Sort notes by size` -> `Files` -> `1188705668` -> `note_size.log`

## Unit tests

Run: `tox`

## Build

1. Build ZIP: `python setup.py dist` (includes unit-tests)
2. Output: `./dist/note-size-X.X-X.zip`

## Release

1. Increment version:
    1. Major: `bumpversion major`
    2. Minor: `bumpversion minor`
    3. Patch: `bumpversion patch`