set -e

src_dir=$(pwd)/note_size
dest_dir=$1

echo "Source dir: $src_dir"
echo "Destination dir: $dest_dir"

if [ ! -d "$src_dir" ]
then
	echo "Source dir absents"
	exit 1
fi

if [ ! -d "$dest_dir" ]
then
	echo "Destination dir absents"
	exit 1
fi

dest_files=$dest_dir/*
echo "Deleting dest files: $dest_files"
rm -rf $dest_files

echo "Copying files..."
cp -r $src_dir/* $dest_dir

echo "Deleting caches"
rm -rf $dest_dir/**/__pycache__
rm -rf $dest_dir/__pycache__

echo "Done"