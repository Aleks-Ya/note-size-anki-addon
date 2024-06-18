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

cache_dir=$dest_dir/__pycache__
echo "Deleting cache: $cache_dir"
rm -rf $cache_dir


python_files=$dest_dir/*.py
echo "Deleting Python files: $python_files"
rm -rf $python_files $dest_dir/icon

echo "Copying files..."
cp $src_dir/*.py $dest_dir
cp -r $src_dir/icon $dest_dir
cp -r $src_dir/config.json $dest_dir

echo "Done"