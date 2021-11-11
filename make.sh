#! /bin/sh

rm -rf dist
rm -rf rubis.egg-info

python3 setup.py bdist_wheel

echo Done.
echo local install
echo 'python3 -m pip install dist/rubis-0.4.2-py3-none-any.whl --upgrade'

echo upload pypi
echo 'python3 -m twine upload --repository pypi dist/*'
