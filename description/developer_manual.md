# User manual for "Note Size" Anki addon

### Logs

See [Logging Level](configuration.md#logging-level)

### Tests

- Run unit-tests: `tox`
- [Manual test cases](../docs/manual_test_cases.md)

### Local deploy

Run: `./deploy_locally.sh ~/.local/share/Anki2/addons21/1188705668`

### Build

1. Build ZIP: `python setup.py dist` (includes unit-tests)
2. Output: `./dist/note-size-X.X-X.zip`

### Generate MarkDown table of content (TOC)

1. Install: `pip install md-toc`
2. Generate TOC:
    1. Features: `md_toc -s 1 github description/features.md`
    2. Configuration: `md_toc -s 1 github description/configuration.md`

### Release

1. Update `CHANGELOG.md` manually
2. Increment version:
    1. Major: `bump-my-version bump major`
    2. Minor: `bump-my-version bump minor`
    3. Patch: `bump-my-version bump patch`
3. Build ZIP: `python setup.py dist`
4. Upload ZIP to the Addon page: https://ankiweb.net/shared/info/1188705668
5. Push Git branch and tags: `git push --follow-tags`
6. Create a GitHub release from tag
