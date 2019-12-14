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

"""Defines a :class:`Frame` that is used for all :module:`simplequi` display"""

from typing import Callable, Optional, Tuple

from ._app import TheApp
from ._canvas import Canvas
from ._fonts import get_text_width_for_font_spec, FontSpec
from ._widgets import Control, MainWidget


class Frame:
    """Frame that contains all other graphical widgets

    :param title: the text to use in the frame title bar
    :param canvas_width: the width of the drawing canvas part of the frame
    :param canvas_height: the height of the drawing canvas part of the frame
    :param control_width: the optional width of the controls (buttons etc.) part of the frame
    """

    def __init__(self, title, canvas_width, canvas_height, control_width=None):
        # type: (str, int, int, Optional[int]) -> None
        TheApp.add_tracked(self)  # Tell app to not close while self is open

        self.__main_widget = MainWidget(title, canvas_width, canvas_height, control_width)
        self.__main_widget.closed.connect(self.__on_main_widget_closed)
        self.__main_widget.show()

    # Internal
    def __on_main_widget_closed(self):
        """Removes reference to allow garbage collection."""
        self.__main_widget = None
        TheApp.remove_tracked(self)  # App can now possibly close

    def set_canvas_background(self, colour):
        # type: (str) -> None
        """Changes the background colour of the frame's canvas, which defaults to black.

        ..seealso:: :func:`~simplequi._colours.get_colour` defines the allowed colour definitions

        :param colour: the background colour to set, accepts any valid CSS colour
        """
        self.__main_widget.drawing_area.set_background_colour(colour)

    def start(self):
        """Commences event handling on the frame (actually on the canvas that handles the events)"""
        self.__main_widget.canvas.start()

    @staticmethod
    def get_canvas_textwidth(text, size, face):
        # type: (str, int, str) -> int
        """Given a text string, a font size, and a font face, this returns the width of the text in pixels.

        It does not draw the text. This is useful in computing the position to draw text when you want it centered or
        right justified in some region. The supported font faces are the default 'serif', 'sans-serif', and 'monospace'.

        :param text: the text to measure
        :param size: the font size that would be drawn with
        :param face: the font face that would be drawn with
        :return: the width of the text in pixels
        """
        return get_text_width_for_font_spec(text, FontSpec(size, face))

    def add_label(self, text, width=None):
        # type: (str, Optional[int]) -> Control
        """Adds a text label to the control panel.

        The width of the label defaults to fit the width of the given text, but can be specified in pixels. If the
        provided width is less than that of the text, the text overflows the label.

        :param text: the label text
        :param width: the optional label width
        :return: a handle that can be used to get and set the label text
        """
        return self.__main_widget.controls.add_label(text, width)

    def add_button(self, text, button_handler, width=None):
        # type: (str, Callable[[], None], Optional[int]) -> Control
        """Adds a button to the frame's control panel with the given text label.

        The width of the button defaults to fit the given text, but can be specified in pixels. If the provided width is
        less than that of the text, the text overflows the button.  The handler should be defined with no parameters.

        :param text: the button text
        :param button_handler: a function to call when the button is clicked
        :param width: the optional button width
        :return: a handle that can be used to get and set the button text
        """
        return self.__main_widget.controls.add_button(text, button_handler, width)

    def add_input(self, text, input_handler, width):
        # type: (str, Callable[[str], None], int) -> Control
        """Adds a text input field to the control panel with the given text label.

        The input field has the given width in pixels. The handler should be defined with one parameter. This parameter
        will receive a string of the text input when the user presses the Enter key.

        :param text: the text of the input field label
        :param input_handler: a function that is called when the user presses enter in the text input field
        :param width: the width of the input field
        :return: a handle that can be used to get and set the input field text
        """
        return self.__main_widget.controls.add_input(text, input_handler, width)

    def set_keydown_handler(self, key_handler):
        # type: (Callable[[int], None]) -> None
        """Adds a keyboard event handler waiting for keydown event.

        When any key is pressed, the keydown handler is called once. The handler should be defined with one parameter.
        This parameter will receive an integer representing a keyboard character.

        :param key_handler: a function to call when a key is pressed down and the frame is focused
        """
        self.__main_widget.canvas.set_keydown_handler(key_handler, self.__main_widget.controls.on_keydown)

    def set_keyup_handler(self, key_handler):
        # type: (Callable[[int], None]) -> None
        """Adds a keyboard event handler waiting for keyup event.

        When any key is released, the keyup handler is called once. The handler should be defined with one parameter.
        This parameter will receive an integer representing a keyboard character.

        :param key_handler: a function to call when a key is released and the frame is focused
        """
        self.__main_widget.canvas.set_keyup_handler(key_handler, self.__main_widget.controls.on_keyup)

    def set_mouseclick_handler(self, mouse_handler):
        # type: (Callable[[tuple], None]) -> None
        """Adds a mouse event handler waiting for mouseclick event.

        When a mouse button is clicked, i.e., pressed and released, the mouseclick handler is called once. The handler
        should be defined with one parameter. This parameter will receive a pair of screen coordinates, i.e., a tuple of
        two non-negative integers.

        :param mouse_handler: a function to call when the mouse is clicked
        """
        self.__main_widget.canvas.set_mouseclick_handler(mouse_handler, self.__main_widget.controls.on_mouseclick)

    def set_mousedrag_handler(self, mouse_handler):
        # type: (Callable[[Tuple[int, int]], None]) -> None
        """Adds a mouse event handler waiting for mousedrag event.

        When a mouse is dragged while the mouse button is being pressed, the mousedrag handler is called for each new
        mouse position. The handler should be defined with one parameter. This parameter will receive a pair of screen
        coordinates, i.e., a tuple of two non-negative integers.

        :param mouse_handler: a function to call when the mouse is clicked and dragged
        """
        self.__main_widget.canvas.set_mousedrag_handler(mouse_handler, self.__main_widget.controls.on_mousedrag)

    def set_draw_handler(self, draw_handler):
        # type: (Callable[[Canvas], None]) -> None
        """Adds an event handler that is responsible for all drawing.

        The handler should be defined with one parameter. This parameter will receive a
        :class:`~simplequi._canvas.Canvas` object.

        :param draw_handler: function to call every 1/60:sup:`th` of a second (actually 17ms), which gets a
            :class:`~simplequi._canvas.Canvas` object as an argument
        """
        self.__main_widget.canvas.set_draw_handler(draw_handler)
