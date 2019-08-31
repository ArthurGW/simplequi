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
from typing import Any
from typing import Callable
from typing import Optional
from typing import Tuple

from PySide2.QtWidgets import QWidget

from _colours import get_colour


class Frame:
    """Singleton Frame containing all other widgets"""

    def __init__(self, title, canvas_width, canvas_height, control_width=None):
        # type: (str, int, int, Optional[int]) -> None
        """Create a frame"""
        self.__main_widget = QWidget()
        self.__controls = []

        self._reset(title, canvas_width, canvas_height, control_width)

    def set_canvas_background(self, colour):
        # type: (str) -> None
        """Changes the background colour of the frame 's canvas, which defaults to black"""
        colour = get_colour(colour)
        raise NotImplementedError

    def start(self):
        """Commence event handling on the frame"""
        raise NotImplementedError

    def get_canvas_textwidth(self, text, size, face):
        # type: (str, int, str) -> int
        """Given a text string, a font size, and a font face, this returns the width of the text in pixels.

        It does not draw the text. This is useful in computing the position to draw text when you want it centered or
        right justified in some region. The supported font faces are the default 'serif', 'sans-serif', and 'monospace'.
        """
        raise NotImplementedError

    def add_label(self, text, width=None):
        # type: (str, Optional[int]) -> Label
        """Adds a text label to the control panel

        The width of the label defaults to fit the width of the given text, but can be specified in pixels. If the
        provided width is less than that of the text, the text overflows the label.
        """
        raise NotImplementedError

    def add_button(self, text, button_handler, width=None):
        # type: (str, Callable[[], None], Optional[int]) -> Button
        """Adds a button to the frame's control panel with the given text label.

        The width of the button defaults to fit the given text, but can be specified in pixels. If the provided width is
        less than that of the text, the text overflows the button.  The handler should be defined with no parameters.
        """
        raise NotImplementedError

    def add_input(self, text, input_handler, width):
        # type: (str, Callable[[str], None], int) -> InputField
        """Adds a text input field to the control panel with the given text label.

        The input field has the given width in pixels. The handler should be defined with one parameter. This parameter
        will receive a string of the text input when the user presses the Enter key.
        """
        raise NotImplementedError

    def set_keydown_handler(self, key_handler):
        # type: (Callable[[int], None]) -> None
        """Add keyboard event handler waiting for keydown event.

        When any key is pressed, the keydown handler is called once. The handler should be defined with one parameter.
        This parameter will receive an integer representing a keyboard character."""
        raise NotImplementedError

    def set_keyup_handler(self, key_handler):
        # type: (Callable[[int], None]) -> None
        """Add keyboard event handler waiting for keyup event.

        When any key is released, the keyup handler is called once. The handler should be defined with one parameter.
        This parameter will receive an integer representing a keyboard character."""
        raise NotImplementedError

    def set_mouseclick_handler(self, mouse_handler):
        # type: (Callable[[tuple], None]) -> None
        """Add mouse event handler waiting for mouseclick event.

        When a mouse button is clicked, i.e., pressed and released, the mouseclick handler is called once. The handler
        should be defined with one parameter. This parameter will receive a pair of screen coordinates, i.e., a tuple of
        two non-negative integers.
        """
        raise NotImplementedError

    def set_mousedrag_handler(self, mouse_handler):
        # type: (Callable[[Tuple[int, int]], None]) -> None
        """Add mouse event handler waiting for mousedrag event.

        When a mouse is dragged while the mouse button is being pressed, the mousedrag handler is called for each new
        mouse position. The handler should be defined with one parameter. This parameter will receive a pair of screen
        coordinates, i.e., a tuple of two non-negative integers."""
        raise NotImplementedError

    def set_draw_handler(self, draw_handler):
        # type: (Callable[[Canvas], None]) -> None
        """Adds an event handler that is responsible for all drawing.

        The handler should be defined with one parameter. This parameter will receive a canvas object."""
        raise NotImplementedError

    # Internal API - not designed to be used by users of the package, but necessary to be on this class
    def _reset(self, title, canvas_width, canvas_height, control_width=None):
        """Destroys all widgets associated with this frame, stops handlers running, sets params to new values.

        Not designed to be used by users"""
        pass

    def _show(self):
        """Actually display the frame"""
        pass


FRAME = Frame('', 1, 1)


def get_new_frame(title, canvas_width, canvas_height, control_width=None):
    # type: (str, int, int, Optional[int]) -> Frame
    """Reset the previous frame and return a new design"""
    FRAME._reset(title, canvas_width, canvas_height, control_width)
    FRAME._show()
    return FRAME
