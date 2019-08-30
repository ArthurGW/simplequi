from os import path
from setuptools import setup

this_dir = path.dirname(__file__)
readme_path = path.join(this_dir, 'README.md')

with open(readme_path, 'w') as readme_file:
    README = readme_file.read()

setup(
    name='simplequi',
    version='0.0.1',
    description='Run codeskulptor.org programs on the desktop using Qt/PySide2',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/ArthurGW/simplequi',
    author='Arthur Gordon-Wright',
    author_email='simplequi.codeskulptor@gmail.com',
    license='GPLv3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    packages=['simplequi'],
    # include_package_data=True,  Might be relevant later
    install_requires=[],
    extras_require={
        'dev': [
            'wheel',
            'setuptools',
            'bumpversion',
        ],
    },
)