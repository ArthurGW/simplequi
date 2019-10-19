bump2version %1 --verbose
python setup.py bdist_wheel
docs/make html
