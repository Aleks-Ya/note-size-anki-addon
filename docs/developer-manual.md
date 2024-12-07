# Developer manual

**Table of content**

<!--TOC-->

- [Setup Python virtual environment](#setup-python-virtual-environment)
- [Logs](#logs)
- [Tests](#tests)
- [SonarQube](#sonarqube)
- [Local deploy](#local-deploy)
- [Build](#build)
- [Execute GitHub Actions locally](#execute-github-actions-locally)
- [Render documentation](#render-documentation)
- [Release](#release)

<!--TOC-->

---

## Setup Python virtual environment

1. Install Tox:
    1. Install PIPX: `pip install pipx`
    2. Install Tox: `pipx install tox`
2. Install PyEnv:
    1. Install PyEnv: `brew install pyenv`
    2. Install VirtualEnv: `brew install pyenv-virtualenv`
3. Create virtual environment:
    1. `pyenv install 3.9.18`
    2. `pyenv virtualenv 3.9.18 note-size-anki-addon`
4. Install Anki packages
    1. Activate virtual environment: `pyenv activate note-size-anki-addon`
    2. Install packages: `pip install -r requirements.txt`

## Logs

See [Logging Level](configuration.md#logging)

## Tests

Run automated tests:

1. Prerequisites: [Setup Python virtual environment](#setup-python-virtual-environment)
2. Activate virtual environment: `pyenv activate note-size-anki-addon`
3. Run unit-tests: `tox`

Run all tests except performance tests: `pytest -m "not performance"`

[Manual test cases](manual-test-cases.md)

## SonarQube

Report at [SonarCloud](https://sonarcloud.io/project/overview?id=Aleks-Ya_note-size-anki-addon)

## Local deploy

Run: `./deploy_locally.sh ~/.local/share/Anki2/addons21/1188705668`

## Build

1. Build ZIP: `python setup.py dist` (includes unit-tests)
2. Output: `./dist/note-size-X.X-X.zip`

## Execute GitHub Actions locally

1. Install `act`: `brew install act`
2. Run: `act`

## Render documentation

1. Install: `pip install md-toc`
2. Edit documentation in `docs-template` folder
3. Update documentation: `./docs_render.sh`
4. Output docs: `docs` folder
5. Commit `docs` folder

## Release

1. Check SonarQube warnings: https://sonarcloud.io/project/overview?id=Aleks-Ya_note-size-anki-addon
2. Update `CHANGELOG.md` manually
3. Update documentation: `./docs_render.sh`
4. Increment version:
    1. Major: `bump-my-version bump major`
    2. Minor: `bump-my-version bump minor`
    3. Patch: `bump-my-version bump patch`
5. Build ZIP: `python setup.py dist`
6. Upload ZIP to the Addon page: https://ankiweb.net/shared/info/1188705668
7. Push Git branch and tags: `git push --follow-tags`
8. Create a GitHub release from tag
