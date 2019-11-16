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

from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication

from ._constants import DOCS_BUILD


class _AppWithRunningFlag(QApplication):
    """Self-starting QApplication with property to say whether it has already been exec_ed"""

    __is_running = False

    #: a set of objects the application will monitor to try and work out when to quit
    tracked = set([])  # Keep track of timers and sounds to know when to quit

    def __init__(self):
        super().__init__([])
        self.__is_running = False
        self.setQuitOnLastWindowClosed(False)  # Since the app needs to stay open if timers are running
        self.lastWindowClosed.connect(self.__queue_check_for_exit)

    def exec_(self):
        """Start the app"""
        if not self.is_running:
            self.__is_running = True
            super().exec_()

    def exit(self, retcode=0):
        # type: (int) -> None
        """Exit the app

        :param retcode: the return code of the app
        """
        self.__is_running = False
        super().exit(retcode)

    @property
    def is_running(self):
        """Whether the app is currently running (has been exec_ed)"""
        return self.__is_running

    def add_tracked(self, obj):
        # type: (object) -> None
        """Keep an eye on when ``stop`` is called on ``obj``.

        Note that it is up to the object itself to actually call :meth:`remove_tracked` when it is stopped.

        :param obj: the object to monitor
        """
        self.tracked.add(obj)

    def remove_tracked(self, obj):
        # type: (object) -> None
        """Timer/sound has stopped so remove and check if all objects are done (i.e. ready to quit)

        :param obj: the object that has stopped
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
        """If no tracked timers or sounds, or no frames exist, it is time to stop"""
        if not self.tracked and not self.topLevelWidgets():
            # Done
            self.exit()


def get_app():
    """Get the application instance unless building docs"""
    if DOCS_BUILD:
        from unittest.mock import Mock
        app = Mock()
    elif QApplication.instance() is None:
        app = _AppWithRunningFlag()
    else:
        app = QApplication.instance()

    return app


def start_app():
    """Get an run an instance of the app to enter the event loop"""
    get_app().exec_()


# Always run the app, once the setup script is done
# This will enter the event loop, which will exit once any frames, timers and sounds created are done
# When building docs, this just calls a Mock so does nothing
atexit.register(start_app)
