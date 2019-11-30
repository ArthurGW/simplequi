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
import os

from unittest.mock import MagicMock

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication


class _AppWithRunningFlag(QApplication):
    """Self-starting QApplication with property to say whether it has already been exec_ed"""

    def __init__(self):
        super().__init__([])
        self.__is_running = False
        #: a set of objects the application will monitor to try and work out when to quit
        self.tracked = set([])  # Keep track of timers and sounds to know when to quit

        self.setQuitOnLastWindowClosed(False)  # Since the app needs to stay open if timers, sounds etc. are running

        atexit.register(self.exec_)

    def exec_(self):
        """Start the app"""
        print('asdasda')
        if not self.is_running:
            self.__is_running = True
            super().exec_()

    def exit(self, retcode=0):
        # type: (int) -> None
        """Exit the app

        :param retcode: the return code of the app
        """
        self.__is_running = False
        self.tracked = set([])
        super().exit(retcode)

    @property
    def is_running(self):
        """Whether the app is currently running (has been exec_ed)"""
        return self.__is_running

    def add_tracked(self, obj):
        # type: (object) -> None
        """Add an object that will prevent the app closing until this object removes itself from tracking

        Note that it is up to the object itself to actually call :meth:`remove_tracked` when appropriate.

        :param obj: the object to monitor
        """
        self.tracked.add(obj)

    def remove_tracked(self, obj):
        # type: (object) -> None
        """Object doesn't require tracking any more so remove and check if all objects are done (i.e. ready to quit)

        :param obj: the object to be removed
        """
        if obj in self.tracked:
            self.tracked.remove(obj)
        self.__queue_check_for_exit()

    def __queue_check_for_exit(self, wait=100):
        # type: (int) -> None
        """Check whether to exit, but return to event loop first to allow queued deletions to take place

        :param wait: the time in ms to wait until checking, defaults to 100
        """
        QTimer.singleShot(wait, self.__check_for_exit)

    def __check_for_exit(self):
        """If no tracked timers, sounds or frames exist, it is time to stop"""
        if not self.tracked:
            # Done
            self.exit()


# Set the application instance unless building docs when a mock is used
if os.getenv('DOCS_BUILD', False):
    TheApp = MagicMock(spec_set=_AppWithRunningFlag)
else:
    TheApp = _AppWithRunningFlag()

# Prevent re-instantiation
del _AppWithRunningFlag
