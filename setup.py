import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="note_size_anki_addon",
    version="1.0",
    author="Alexey Yablokov",
    description="Note Size Anki addon",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aleks-Ya/note-size-anki-addon",
    packages=setuptools.find_packages()
)
