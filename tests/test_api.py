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

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication

import simplequi
from simplequi._keys import REVERSE_KEY_MAP


class TestAPI(unittest.TestCase):
    """Basic API sanity checks"""

    def test_create_frame(self):
        """Test basic parameters are passed to correct parts of frame"""
        frame = simplequi.create_frame('FRAME', 123, 200, control_width=150)
        self.assertEqual(frame._Frame__main_widget.windowTitle(), 'FRAME')
        self.assertEqual(frame._Frame__main_widget.drawing_area.canvas.width(), 123)
        self.assertEqual(frame._Frame__main_widget.drawing_area.canvas.height(), 200)
        self.assertEqual(frame._Frame__main_widget.controls.width(), 150)
        frame._Frame__main_widget.close()

    def test_create_timer(self):
        """Test a timer running 10 callback at 10ms intervals"""
        self.calls = 0

        def callback():
            self.calls += 1
            if self.calls == 10:
                self.timer.stop()

        self.timer = simplequi.create_timer(10, callback)
        self.timer.start()
        self.assertTrue(self.timer.is_running())
        # Enter the event loop to wait for the timer to finish
        QApplication.instance().exec_()
        self.assertFalse(self.timer.is_running())
        self.assertEqual(self.calls, 10)

    def test_key_map(self):
        """Test all keys in map and reverse mapped to same value"""
        _dummy = simplequi.KEY_MAP['space']
        self.assertEqual(67, len(simplequi.KEY_MAP))  # Initialised by value lookup

        special_keys = {
            'left': '⭠',
            'right': '⭢',
            'up': '⭡',
            'down': '⭣'
        }

        # Test known keys
        for key, val in simplequi.KEY_MAP.items():
            if key in special_keys:
                self.assertEqual(special_keys[key], REVERSE_KEY_MAP[val], 'mismatch in forward and reverse key maps')
            else:
                self.assertEqual(key, REVERSE_KEY_MAP[val], 'mismatch in forward and reverse key maps')

        # Test unknown keys
        for key in {Qt.Key_Enter, Qt.Key_Backspace, Qt.Key_Tab}:
            self.assertNotIn(key, REVERSE_KEY_MAP)
            self.assertEqual(REVERSE_KEY_MAP[key], '<{}>'.format(key))
            self.assertIn(key, REVERSE_KEY_MAP)

    def test_load_image(self):
        """Test image is loaded"""
        os.chdir(os.path.dirname(__file__))
        image = simplequi.load_image('../simplequi/examples/resources/sample_image.png')
        timer = simplequi.create_timer(100, QApplication.instance().exit)
        QApplication.instance().exec_()
        self.assertEqual(image.get_width(), 1000)
        self.assertEqual(image.get_height(), 1200)

    def test_load_sound(self):
        """Test MP3 and WAV sounds are loaded"""
        os.chdir(os.path.dirname(__file__))
        sound = simplequi.load_sound('../simplequi/examples/resources/425556__planetronik__rock-808-beat.mp3')
        sound2 = simplequi.load_sound('../simplequi/examples/resources/253756_tape-on.wav')
        timer = simplequi.create_timer(200, QApplication.instance().exit)
        QApplication.instance().exec_()
        self.assertTrue(sound._Sound__sound_loaded)
        self.assertTrue(sound2._Sound__sound_loaded)


if __name__ == '__main__':
    unittest.main()
