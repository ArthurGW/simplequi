bump2version %1 --verbose
python setup.py bdist_wheel
CALL docs/make.bat clean
CALL docs/make.bat html
