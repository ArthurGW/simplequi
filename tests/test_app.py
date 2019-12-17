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
from unittest.mock import patch

from PySide2.QtWidgets import QApplication

# This import is just used for ensuring the app is initialized, hence the ignore below
import simplequi  # noqa: F401


class TestApp(unittest.TestCase):
    """Test application tracking of objects and exit checking"""
    def setUp(self):
        self.app = QApplication.instance()

    def test_app(self):
        """Test adding and removing objects"""
        # These mocks need to be here so the app can exit properly after this method ends
        with patch('PySide2.QtWidgets.QApplication.exit') as exit_func:
            with patch.object(self.app, '_AppWithRunningFlag__queue_check_for_exit') as queue_check:
                queue_check.side_effect = self.app._AppWithRunningFlag__check_for_exit
                # Starts empty
                self.assertSetEqual(self.app.tracked, set([]))

                # Add two objects
                obj = object()
                obj2 = object()
                self.app.add_tracked(obj)
                self.app.add_tracked(obj2)
                self.assertSetEqual(self.app.tracked, {obj, obj2})

                # Checking for exit should not exit with tracked objects
                queue_check()
                exit_func.assert_not_called()

                # Remove one and check exit not called
                self.app.remove_tracked(obj2)
                self.assertSetEqual(self.app.tracked, {obj})
                queue_check.assert_has_calls([])
                exit_func.assert_not_called()

                # Remove the last one, exit should now be called
                self.app.remove_tracked(obj)
                self.assertSetEqual(self.app.tracked, set([]))
                queue_check.assert_has_calls([])
                exit_func.assert_called_once_with(0)


if __name__ == '__main__':
    unittest.main()
