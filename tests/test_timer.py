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

from PySide2.QtWidgets import QApplication

import simplequi


class TestTimer(unittest.TestCase):
    """Tested separately from other API as it needs to run in the event loop"""

    def test_create_timer(self):
        self.calls = 0

        def callback():
            nonlocal self
            self.calls += 1
            if self.calls == 10:
                self.timer.stop()

        self.timer = simplequi.create_timer(10, callback)
        self.timer.start()
        self.assertTrue(self.timer.is_running())
        # Enter the event loop to wait for the timer
        QApplication.instance().exec_()
        self.assertFalse(self.timer.is_running())
        self.assertEqual(self.calls, 10)


if __name__ == '__main__':
    unittest.main()
