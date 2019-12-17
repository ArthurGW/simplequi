# -----------------------------------------------------------------------------
# Copyright ©2019 Arthur Gordon-Wright
# <https://github.com/ArthurGW/simplequi>
# <simplequi.codeskulptor@gmail.com>
#
# This file is part of simplequi.
#
# simplequi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# simplequi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with simplequi.  If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------

import os
from setuptools import setup

this_dir = os.path.dirname(__file__)
readme_path = os.path.join(this_dir, 'README.md')

with open(readme_path, 'r') as readme_file:
    README = readme_file.read()

BUILD_REQUIREMENTS = [
    'bump2version>=0.5.11',
    'wheel>=0.33.6',
]

DOCS_REQUIREMENTS = [
    'sphinx>=2.2',
    'sphinx-rtd-theme>=0.4.3',
    'sphinx-autodoc-typehints[type_comments]',
    'm2r',
]

INSTALL_REQUIREMENTS = []
INSTALL_REQUIREMENTS += ['PySide2>=5.12.0'] if not os.getenv('DOCS_BUILD', False) else []  # Don't use PySide2 on RTD


setup(
    name='simplequi',
    version='1.0.2',
    description='Run codeskulptor.org programs on the desktop using Qt/PySide2',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/ArthurGW/simplequi',
    author='Arthur Gordon-Wright',
    author_email='simplequi.codeskulptor@gmail.com',
    license='GPLv3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        # 'Programming Language :: Python :: 2', Not currently supported, unlikely to change
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=[
        'simplequi',
        'simplequi.examples'
    ],

    # Include OpenSSL dlls so PySide2 can retrieve images/sounds from https URLs
    # This may have legal issues in some countries where encryption is not allowed?
    # TODO: consider whether to keep including this or just provide instructions for how to get it
    package_data={
        'simplequi': ['resources/ssllib/*.*',
                      'resources/fonts/NK57 Monospace/*.*'],
        'simplequi.examples': ['resources/*.*'],
    },
    python_requires='>=3.5',
    install_requires=INSTALL_REQUIREMENTS,
    extras_require={
        'build': BUILD_REQUIREMENTS,
        'dev': BUILD_REQUIREMENTS + DOCS_REQUIREMENTS,
        'docs': DOCS_REQUIREMENTS,
    },
)
