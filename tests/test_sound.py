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

from functools import partial
from unittest.mock import patch, ANY

from PySide2.QtCore import QByteArray, QIODevice, QBuffer, QTimer
from PySide2.QtGui import QPixmap
from PySide2.QtMultimedia import QMediaPlayer
from PySide2.QtNetwork import QNetworkReply
from PySide2.QtWidgets import QApplication

import simplequi


class TestSound(unittest.TestCase):
    """Test Image API"""

    def setUp(self):
        self.played = False

    def wait_for_sound(self, sound, fail=False, play=True, playing=False):
        # Tracked while loading
        self.assertIn(sound, QApplication.instance().tracked)

        def delayed_play():
            if not self.played:
                QTimer.singleShot(10, sound.play)
                self.played = True

        if play and not playing:
            sound._Sound__player.mediaStatusChanged.connect(delayed_play)
            sound.set_volume(0)

        # Record tracked set before pausing sound
        tracked = set([])
        t = simplequi.create_timer(200, lambda: tracked.update(QApplication.instance().tracked))
        t2 = simplequi.create_timer(300, sound.rewind)
        t.start()
        t2.start()
        QApplication.instance().remove_tracked(t)
        QApplication.instance().remove_tracked(t2)
        QApplication.instance().exec_()

        self.assertEqual(sound._Sound__sound_loaded, not fail)
        if fail or not (play or playing):
            self.assertNotIn(sound, tracked)
        elif play:
            # Sound was tracked before pausing
            self.assertIn(sound, tracked)

        self.assertEqual(sound._Sound__player.state(), QMediaPlayer.StoppedState)

    def test_invalid_path(self):
        """Non-existent path doesn't fail but doesn't play either"""
        sound = simplequi.load_sound('not_a_file.wav')
        self.wait_for_sound(sound, fail=True)

    def test_invalid_file(self):
        """Existing but non-sound path doesn't raise errors but doesn't play"""
        sound = simplequi.load_sound(__file__)
        self.wait_for_sound(sound, fail=True)

    @staticmethod
    def __valid_sound():
        os.chdir(os.path.dirname(__file__))
        return simplequi.load_sound('../simplequi/examples/resources/253756_tape-on.wav')

    def test_play_before_load(self):
        """Test play being called while sound is still loading - should play on load"""
        sound = self.__valid_sound()
        sound.play()
        sound.set_volume(0)
        self.wait_for_sound(sound, play=False, playing=True)

    def test_play_after_load(self):
        """Test play being called by something after loading - should add sound to tracked"""
        sound = self.__valid_sound()
        self.wait_for_sound(sound)

    def test_pause(self):
        sound = self.__valid_sound()
        self.wait_for_sound(sound, play=False, playing=False)
        sound.play()
        sound.pause()
        self.assertEqual(sound._Sound__player.state(), QMediaPlayer.PausedState)
        self.assertEqual(sound._Sound__player.position(), 0)

    def test_volume(self):
        sound = self.__valid_sound()
        sound.set_volume(0.67)
        self.assertEqual(sound._Sound__player.volume(), 67)

