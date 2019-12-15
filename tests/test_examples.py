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
import unittest

import simplequi.examples

SCRIPT_CLOSER = """
from PySide2.QtCore import QTimer

try:
    count = 8
    QTimer.singleShot(1000, frame._Frame__main_widget.close)
except (NameError):
    pass
"""


class TestExamples(unittest.TestCase):
    """Run everything from the examples folder"""

    @classmethod
    def factory(cls, path):
        """Generates a test function for the given path"""
        file_name = os.path.splitext(os.path.basename(path))[0]
        test_name = 'test_{}'.format(file_name)

        def run_test(self):
            with open(path) as inp:
                script = inp.read()
                script += SCRIPT_CLOSER

            os.chdir(os.path.dirname(path))
            exec(script, {})

        setattr(cls, test_name, run_test)


examples_path = os.path.dirname(simplequi.examples.__file__)

for path in os.listdir(examples_path):
    full_path = os.path.join(examples_path, path)

    if os.path.isfile(full_path) and path != '__init__.py':
        TestExamples.factory(full_path)

if __name__ == '__main__':
    unittest.main()
