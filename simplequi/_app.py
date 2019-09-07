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

import atexit

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QTimer


class _AppWithRunningFlag(QApplication):
    """Self-starting QApplication with property to say whether it has already been exec_ed"""

    timers = set([])  # Keep track of timers to know when to quit

    def __init__(self):
        super().__init__([])
        self.__is_running = False
        self.setQuitOnLastWindowClosed(False)  # Since the app needs to stay open if timers are running
        self.lastWindowClosed.connect(self.__queue_check_for_exit)

        # Always run the app, once the setup script is done
        # This will enter the event loop, which will exit once any frames and timers created are done
        atexit.register(self.exec_)

    def exec_(self):
        if not self.is_running:
            self.__is_running = True
            super().exec_()

    def exit(self, retcode):
        self.__is_running = False
        super().exit(retcode)

    @property
    def is_running(self):
        return self.__is_running

    def add_timer(self, timer):
        """Keep an eye on when this timer is stopped is done"""
        self.timers.add(timer)

    def remove_timer(self, timer):
        """Timer has stopped so remove and check if all objects are done"""
        self.timers.remove(timer)
        self.__queue_check_for_exit()

    def __queue_check_for_exit(self, wait=100):
        """Check whether to exit, but return to event loop first to allow queued deletions to take place"""
        QTimer.singleShot(wait, self.__check_for_exit)

    def __check_for_exit(self):
        """If no timers or frames exist, it is time to stop"""
        if not self.timers and not self.topLevelWidgets():
            # Done
            self.exit(0)


if not QApplication.instance():
    TheApp = _AppWithRunningFlag()
else:
    TheApp = QApplication.instance()
del _AppWithRunningFlag  # Prevent non-singleton
