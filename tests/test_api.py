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

import unittest

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication

import simplequi
from simplequi._keys import REVERSE_KEY_MAP

# TODO: update and add more tests
class TestAPI(unittest.TestCase):
    """Basic API sanity checks"""

    def test_image(self):
        self.fail('Not implemented')

    def test_sound(self):
        self.fail('Not implemented')

    def test_key_map(self):
        """Test all keys in map and reverse mapped to same value"""
        self.assertEqual(0, len(simplequi.KEY_MAP))  # Map not initialised yet
        _ = simplequi.KEY_MAP['space']
        self.assertEqual(67, len(simplequi.KEY_MAP))  # Initialised by value lookup

        special_keys = {
            'left': '⭠',
            'right': '⭢',
            'up': '⭡',
            'down': '⭣'
        }

        # Test known keys
        for key, val in simplequi.KEY_MAP.items():
            if key in special_keys:
                self.assertEqual(special_keys[key], REVERSE_KEY_MAP[val], 'mismatch in forward and reverse key maps')
            else:
                self.assertEqual(key, REVERSE_KEY_MAP[val], 'mismatch in forward and reverse key maps')

        # Test unknown keys
        for key in {Qt.Key_Enter, Qt.Key_Backspace, Qt.Key_Tab}:
            self.assertNotIn(key, REVERSE_KEY_MAP)
            self.assertEqual(REVERSE_KEY_MAP[key], '<{}>'.format(key))
            self.assertIn(key, REVERSE_KEY_MAP)

    def test_create_frame(self):
        self.fail('Not implemented')


if __name__ == '__main__':
    unittest.main()
