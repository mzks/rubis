#! /bin/sh

rm -rf dist
rm -rf rubis.egg-info

python3 setup.py bdist_wheel

echo Done.
echo local install
echo 'python3 -m pip install dist/rubis-*.whl --upgrade'
