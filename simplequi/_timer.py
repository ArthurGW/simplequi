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
from typing import Callable

from ._app import TheApp

from PySide2.QtCore import QTimer


class StartStopTimer(QTimer):
    """QTimer that registers/unregisters itself with TheApp singleton on start/stop"""

    def start(self, *args):
        super().start()
        TheApp.add_timer(self)

    def stop(self):
        super().stop()
        TheApp.remove_timer(self)


class Timer:
    """Container for a StartStopTimer that fires at a given rate and calls a handler"""

    def __init__(self, interval, timer_handler):
        # type: (int, Callable[[], None]) -> None
        """Creates a timer.

        Once started, it will repeatedly call the given event handler at the specified interval, which is given in
        milliseconds. The handler should be defined with no arguments.
        """
        self.__timer = StartStopTimer()
        self.__timer.setInterval(interval)
        self.__timer.timeout.connect(timer_handler)

    def start(self):
        """Starts or restarts the timer"""
        self.__timer.start()

    def stop(self):
        """Stops the timer.  It can be restarted"""
        self.__timer.stop()

    def is_running(self):
        # type: () -> bool
        """Returns whether the timer is running, i.e., it has been started, but not stopped"""
        return self.__timer.isActive()
