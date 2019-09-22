bump2version %1 --verbose --dry-run
python setup.py bdist_wheel
docs/make html
