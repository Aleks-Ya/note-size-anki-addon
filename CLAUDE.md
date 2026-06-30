# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Note Size is an Anki addon (ID: 1188705668) that displays the size of collections, decks, notes, and attached media files in the Anki flashcard application. It supports multiple Anki versions (earliest, current, beta) via `tox`.

## Commands

### Testing

```bash
# Run all unit tests across all configured environments
tox

# Run tests for a specific environment
tox -e anki-current
tox -e anki-earliest
tox -e anki-beta

# Run a single test file or test (within an active venv)
pytest tests/calculator/test_size_calculator.py
pytest tests/calculator/test_size_calculator.py::TestSizeCalculator::test_something

# Run only integration tests
tox -- tests -m integration

# Skip performance tests
pytest -m "not performance"
```

### Build & Deployment

```bash
# Build ZIP distribution (runs tests first)
./build_dist.sh

# Deploy locally to Anki addons directory
./deploy_locally.sh ~/.local/share/Anki2/addons21/1188705668

# Render documentation from templates
./render_docs.sh
```

### Version Bumping

```bash
bump-my-version bump patch   # or minor / major
```

## Architecture

### Entry Point & Initialization

`note_size/__init__.py` is the Anki addon entry point. It registers an `on_profile_did_open` hook that triggers `profile_hook.py`, which manually wires all dependencies (~40 components) and attaches Anki GUI hooks. There is no DI framework — every dependency is instantiated and injected explicitly in `profile_hook.py`.

### Key Modules

**`calculator/`** — Core size computation. `SizeCalculator` is the central engine: it aggregates note text size and media file sizes, using `UsedFilesCalculator` (which files appear in a note) and `UpdatedFilesCalculator` (which files changed on disk). Results are cached aggressively.

**`cache/`** — Multi-layer caching. `CacheManager` owns all cache instances. Caches are persisted to disk via `CacheStorage` and warmed in a background thread by `CacheInitializer` on profile open. Cache keys use `ItemId` (note ID) and size type (`SizeType` enum: `TOTAL`, `TEXTS`, `FILES`).

**`config/`** — Config is read from `config.json` (Anki's addon config API). `ConfigLoader` deserializes it; `Config` exposes typed accessors. `LevelParser` converts the color-threshold config into `Level` objects. `ConfigHooks` registers Anki hooks to reload config when the user saves it.

**`ui/`** — Four UI integration points, each in its own sub-package:
- `deck_browser/` — Adds size column to the deck list
- `browser/` — Adds sortable size columns to the card browser
- `editor/` — Adds a size button in the note editor toolbar
- `details_dialog/` — Dialog showing per-field and per-file size breakdown

**`common/`** — Shared types (`SizeType`, `ItemId`, etc.), `CollectionHolder` (wraps the live Anki `Collection`), and `NumberFormatter`.

### Test Structure

`tests/` mirrors the `note_size/` source layout. `tests/conftest.py` provides pytest fixtures that mock the Anki `Collection` (using `MagicMock`) so tests run without a real Anki installation.

Pytest markers (defined in `pytest.ini`):
- `performance` — slow benchmarks, excluded by default in CI
- `integration` — tests that need more setup
- `skip_for_beta` / `skip_for_current` / `skip_for_earliest` — version-specific exclusions

### Anki Version Support

`requirements/` contains pinned dependency files per Anki version. `tox.ini` defines an environment per file. `pytest.ini` sets `QT_QPA_PLATFORM=offscreen` for headless CI. The `skip_for_*` markers let individual tests opt out of specific versions.

### Documentation

`docs-template/` contains source templates (including UML diagrams). `docs/` is the rendered output — do not edit `docs/` directly; run `./render_docs.sh` instead.
