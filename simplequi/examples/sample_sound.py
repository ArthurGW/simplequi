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
"""Play some sounds with decreasing volume"""

import simplequi as simplegui
from math import log2

sound = simplegui.load_sound('resources/253756_tape-on.wav')
drums = simplegui.load_sound('resources/425556__planetronik__rock-808-beat.mp3')
volume = 100
count = 100
total_log = log2(volume)


def callback():
    global count, volume
    count -= 1

    fraction = count / 100.
    log_volume = total_log * fraction
    drum_volume = 2 ** log_volume / 100.
    sound_volume = drum_volume * 0.2

    drums.set_volume(drum_volume)
    sound.set_volume(sound_volume)

    if count == 0:
        drum_timer.stop()
        sound_timer.stop()
        volume_timer.stop()
    else:
        drums.play()
        sound.play()


drum_timer = simplegui.create_timer(8000, drums.play)
sound_timer = simplegui.create_timer(4000, sound.play)
volume_timer = simplegui.create_timer(240, callback)

drum_timer.start()
sound_timer.start()
volume_timer.start()
