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

from PySide2.QtWidgets import QApplication


class _AppWithRunningFlag(QApplication):
    """QApplication with property to say whether it has already been exec_ed"""

    def __init__(self):
        super().__init__([])
        self.__is_running = False

    def exec_(self):
        if not self.is_running:
            self.__is_running = True
            super().exec_()

    @property
    def is_running(self):
        return self.__is_running


TheApp = _AppWithRunningFlag()



