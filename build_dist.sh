set -e

if [ "$1" = "--skip-tests" ]; then
    python build_dist.py --skip_unit_tests --skip_integration_tests
else
    python build_dist.py
fi

echo Done
