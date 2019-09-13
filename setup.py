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

setup(
    name='simplequi',
    version='0.6.0',
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
    install_requires=['PySide2>=5.12.0'],  # Currently only support PySide2
    extras_require={
        'dev': [
            'bump2version==0.6.01',
            'PySide2>=5.12.0'
            'setuptools==41.2.0',
            'wheel==0.33.6',
        ],
    },
)