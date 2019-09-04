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
# G_NU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with simplequi.  If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------
"""The basic simplegui API - all package-level calls go through here.

The returned objects from these functions all implement their own APIs defined in their respective modules."""

from typing import Callable
from typing import Optional

from _frame import reset_frame
from _image import Image
from _keys import KEY_MAP
from _sound import Sound
from _timer import Timer

__all__ = ['KEY_MAP',
           'create_frame',
           'create_timer',
           'load_image',
           'load_sound']


def create_frame(title, canvas_width, canvas_height, control_width=None):
    # type: (str, int, int, Optional[int]) -> Frame
    """Creates a new frame for interactive programs.

    The frame's window has the given title, a string.
    The frame consists of two parts: a control panel on the left and a canvas on the right.
    The control panel's width in pixels can be specified by the number control_width.
    The canvas width in pixels is the number canvas_width.
    The height in pixels of both the control panel and canvas is the number canvas_height.
    """
    return reset_frame(title, canvas_width, canvas_height, control_width)


def create_timer(interval, timer_handler):
    # type: (int, Callable[[], None]) -> Timer
    """Creates a timer.

    Once started, it will repeatedly call the given event handler at the specified interval, which is given in ms.
    The handler should be defined with no arguments.
    """
    return Timer(interval, timer_handler)


def load_image(url):
    # type: (str) -> Image
    """
    Loads an image from the specified URL.

    The image can be in any format supported by PySide2.
    No error is raised if the file isn't found or is of an unsupported format.
    """
    return Image.load_image_from_url(url)


def load_sound(url):
    # type: (str) -> Sound
    """
    Loads a sound from the specified URL.

    Supports whatever audio formats that PySide2 supports.
    No error is raised if the file isn't found or is of an unsupported format.
    """
    return Sound.load_sound_from_url(url)
