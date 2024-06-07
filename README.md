# Note Size Anki addon

## Description

See [Addon Description](description/description.md)

## Logs

- From filesystem: `{anki_dir}/addons21/1188705668/note_size.log`
- From Anki main window: `Tools` -> `Add-ons` -> `Note Size...` -> `Files` -> `1188705668` -> `note_size.log`

## Unit tests

Run: `tox`

## Build

Build ZIP: `python setup.py dist` (output `./dist/note-size-1.0-0.zip`)

## Release

1. Increment version:
    1. Major: `bumpversion major`
    2. Minor: `bumpversion minor`
    3. Patch: `bumpversion patch`