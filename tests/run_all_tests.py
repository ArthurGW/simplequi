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

from PySide2.QtCore import QTimer

import simplequi


class AllRunner:
    def __init__(self):
        self.timer = simplequi.create_timer(0, self.run_all)
        self.path = __file__

    def start(self):
        self.timer.start()

    def run_all(self):
        self.timer.stop()
        loader = unittest.TestLoader()
        loader.discover(os.path.dirname(self.path))
        unittest.main(testLoader=loader)

if __name__ == '__main__':
    runner = AllRunner()
    QTimer.singleShot(0, runner.start)
