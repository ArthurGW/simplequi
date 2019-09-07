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

import asyncio
import queue
import time

import unittest

from PySide2.QtCore import QTimer, QThread, QObject, QWaitCondition, QMutex
from PySide2.QtWidgets import QApplication

import simplequi


async def waiter():
    await asyncio.sleep(1)


class Watcher(QObject):
    def __init__(self, watchee):
        super().__init__()
        self.watchee = watchee
        self.t = self.startTimer(100)

    def timerEvent(self, event):
        if self.watchee.calls == 10:
            self.killTimer(self.t)


class TestTimer(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        QApplication.instance().lastWindowClosed.emit()

    def test_create_timer(self):
        self.calls = 0
        # self.thread = QThread()
        # self.watcher = Watcher(self)
        # self.watcher.moveToThread(self.thread)
        # self.calls = queue.Queue(10)
        # t = timer._Timer__timer
        # t.moveToThread(self.thread)
        # self.thread.start()
        # self.thread.wait()

        def callback():
            nonlocal self
            self.calls += 1
            if self.calls == 10:
                self.timer.stop()
                QApplication.instance().exit(0)

        self.timer = simplequi.create_timer(10, callback)
        self.timer.start()
        self.assertTrue(self.timer.is_running())
        # Enter the event loop to wait for the timer
        QApplication.instance().exec_()
        self.assertFalse(self.timer.is_running())
        self.assertEqual(self.calls, 10)


if __name__ == '__main__':
    unittest.main()
