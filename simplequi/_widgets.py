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
from typing import Optional
from typing import Tuple
import sys

from PySide2.QtWidgets import QLabel, QWidget, QFrame, QVBoxLayout

from _colours import get_colour
from simplequi import _app


DEFAULT_CONTROL_PANEL_WIDTH = 100


class EventWidget(QLabel):
    """Control for the keypress and mouse event info panels"""
    def __init__(self, default_string, parent=None, width=100):
        super().__init__(default_string, parent)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setFixedSize(width, 17)


class Frame:
    """Singleton Frame containing all other widgets

    Note the singleton-ness in not strictly enforced here, but the module function 'reset_frame' is the only external
    function that should be used to get Frames, and that simply resets the fixed instance of this class
    """

    __first_init = True

    def __init__(self, title, canvas_width, canvas_height, control_width=None):
        # type: (str, int, int, Optional[int]) -> None
        """Create a frame"""
        if self.__first_init:
            # This actually gets deleted by reset but this is the easiest way to do it
            self.__main_widget = QWidget()

        # Actually setup the UI
        self.__reset(title, canvas_width, canvas_height, control_width)

        if not self.__first_init:
            # The first init is a dummy one to create the singleton, hence only show window on future inits
            self.__main_widget.show()
        else:
            self.__first_init = False

    def set_canvas_background(self, colour):
        # type: (str) -> None
        """Changes the background colour of the frame 's canvas, which defaults to black"""
        colour = get_colour(colour)
        raise NotImplementedError

    @staticmethod
    def start():
        """Commence event handling on the frame"""
        sys.exit(_app.exec_())

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

    # Internal API
    def __reset(self, title, canvas_width, canvas_height, control_width=None):
        # type: (str, int, int, Optional[int]) -> None
        """Destroys all widgets associated with this frame, stops handlers running, sets params to new values"""
        # Destroy old widget, which cascades down to all child widgets, and create new
        self.__main_widget.deleteLater()
        self.__main_widget = QWidget()

        # Basic window layout
        self.__main_widget.setWindowTitle(title)
        control_width = DEFAULT_CONTROL_PANEL_WIDTH if control_width is None else control_width
        total_width = canvas_width + control_width
        total_height = canvas_height
        self.__main_widget.setFixedSize(total_width, total_height)

        # Widgets layout
        self.__main_layout = QVBoxLayout()
        self.__controls = [EventWidget('Key: ', self.__main_widget), EventWidget('Mouse: ', self.__main_widget)]
        for cont in self.__controls:
            self.__main_layout.addWidget(cont)
        self.__main_widget.setLayout(self.__main_layout)


# Create singleton Frame with dummy params
FRAME = Frame('', 1, 1, DEFAULT_CONTROL_PANEL_WIDTH)


def reset_frame(title, canvas_width, canvas_height, control_width=None):
    # type: (str, int, int, Optional[int]) -> Frame
    """Reset the previous frame and return singleton"""
    Frame.__init__(FRAME, title, canvas_width, canvas_height, control_width)
    return FRAME
