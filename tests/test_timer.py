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
from unittest.mock import Mock, call

from PySide2.QtWidgets import QApplication

import simplequi


class TestTimer(unittest.TestCase):
    """Tested Timer API"""

    def setUp(self):
        self.handler = Mock()
        self.app = QApplication.instance()

    def test_timer(self):
        timer = simplequi.create_timer(100, self.handler)
        self.assertFalse(timer.is_running())
        self.assertNotIn(timer, self.app.tracked)
        timer.start()
        self.assertTrue(timer.is_running())
        self.assertIn(timer, self.app.tracked)
        timer.stop()
        self.assertFalse(timer.is_running())
        self.assertNotIn(timer, self.app.tracked)

    def test_handler(self):
        timer = simplequi.create_timer(8, self.handler)
        stop_timer = simplequi.create_timer(40, timer.stop)
        exit_timer = simplequi.create_timer(50, self.app.exit)
        timer.start()
        stop_timer.start()
        exit_timer.start()
        self.app.exec_()
        self.assertAlmostEqual(self.handler.call_count, 5, delta=1)  # Allow delta due to timer inaccuracies
        self.handler.assert_has_calls([call() for _ in range(self.handler.call_count)])


if __name__ == '__main__':
    unittest.main()
