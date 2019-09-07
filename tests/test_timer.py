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
import asyncio

from PySide2.QtCore import QTimer

import simplequi


async def waiter():
    await asyncio.sleep(1)


class AsyncTestCase(unittest.TestCase):
    @unittest.skip("Can't make this work yet")
    def runTest(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.create_timer_test())

    async def create_timer_test(self):
        calls = 0

        def callback():
            nonlocal timer, calls
            calls += 1
            print(calls)
            if calls == 10:
                timer.stop()

        timer = simplequi.create_timer(10, callback)
        timer.start()
        self.assertTrue(timer.is_running())

        await waiter()

        self.assertFalse(timer.is_running())
        self.assertEqual(calls, 10)


if __name__ == '__main__':
    QTimer.singleShot(0, unittest.main)
