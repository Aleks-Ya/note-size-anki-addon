set -e

if [ "$(ls -A docs)" ]; then
   rm -r docs/*
fi

rsync -a --exclude='images-krita' --exclude='uml' docs-template/ docs/

files_with_toc=("configuration.md" "features.md" "developer-manual.md")
for file in "${files_with_toc[@]}"; do
  md_toc -p -s 1 github docs/$file
done
