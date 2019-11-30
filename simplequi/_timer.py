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
"""Contains a single class :class:`Timer` that is used to fire events at known intervals."""

from typing import Callable

from ._app import TheApp

from PySide2.QtCore import QTimer


class Timer:
    """Creates a timer.

    Once started, it will repeatedly call the given event handler at the specified interval, which is given in
    milliseconds. The handler should be defined with no arguments.

    :param interval: how often to call the ``timer_handler``
    :param timer_handler: a function to call every ``interval`` milliseconds
    """

    def __init__(self, interval, timer_handler):
        # type: (int, Callable[[], None]) -> None
        self.__timer = QTimer()
        self.__timer.setInterval(interval)
        self.__timer.timeout.connect(timer_handler)

    def start(self):
        """Starts or restarts the timer."""
        self.__timer.start()
        TheApp.add_tracked(self)

    def stop(self):
        """Stops the timer. It can be restarted."""
        self.__timer.stop()

        # Tell the app it can close if this timer is all it is waiting for:
        TheApp.remove_tracked(self)

    def is_running(self):
        # type: () -> bool
        """Returns whether the timer is running, i.e., it has been started, but not stopped."""
        return self.__timer.isActive()
