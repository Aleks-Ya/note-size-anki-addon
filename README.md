# Note Size Anki addon

## Description

See [Addon Description](description/description.md)

## Logs

`Tools` -> `Add-ons` -> `Note Size - sort notes by size` -> `Files` -> `1188705668` -> `note_size.log`

## Unit tests

Run: `tox`

## Local deploy

Run: `./deploy_locally.sh ~/.local/share/Anki2/addons21/1188705668`

## Build

1. Build ZIP: `python setup.py dist` (includes unit-tests)
2. Output: `./dist/note-size-X.X-X.zip`

## Release

1. Increment version:
    1. Major: `bumpversion major`
    2. Minor: `bumpversion minor`
    3. Patch: `bumpversion patch`